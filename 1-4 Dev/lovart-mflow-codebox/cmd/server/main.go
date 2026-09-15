package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

// ============================================================
// Data models
// ============================================================

type PipelineItem struct {
	ID          string      `json:"id"`
	Category    string      `json:"category"`
	TargetType  string      `json:"target_type"`
	Stage       string      `json:"stage"`
	Phase       string      `json:"phase"`
	Agent       string      `json:"agent"`
	Skill       string      `json:"skill"`
	ArtifactPath string     `json:"artifact_path"`
	QA          QAInfo      `json:"qa"`
	Publish     PublishInfo `json:"publish"`
	FixCount    int         `json:"fix_count"`
	CreatedAt   string      `json:"created_at"`
	UpdatedAt   string      `json:"updated_at"`
	History     []HistoryEntry `json:"history"`
}

type QAInfo struct {
	L1Block  *int   `json:"l1_block"`
	L2Block  *int   `json:"l2_block"`
	L7Block  *int   `json:"l7_block"`
	LastRun  string `json:"last_run"`
	FixCount int    `json:"fix_count"`
}

type PublishInfo struct {
	SanityID    string `json:"sanity_id"`
	ImportedAt  string `json:"imported_at"`
	Status      string `json:"status"`
}

type HistoryEntry struct {
	Ts      string `json:"ts"`
	From    string `json:"from"`
	To      string `json:"to"`
	Reason  string `json:"reason"`
	Agent   string `json:"agent"`
}

type Decision struct {
	Stage          string   `json:"stage"`
	Scenario       string   `json:"scenario"`
	ProfileTarget  string   `json:"profile_target"`
	Action         string   `json:"action"`
	Skills         []string `json:"skills"`
	Reason         string   `json:"reason"`
}

type HookResult struct {
	Check  string `json:"check"`
	Status string `json:"status"` // PASS / BLOCK / WARN
	Detail string `json:"detail"`
}

// ============================================================
// In-memory store (replace with MongoDB later)
// ============================================================

type Store struct {
	mu        sync.RWMutex
	items     map[string]*PipelineItem
	decisions []Decision
}

var store = &Store{
	items: make(map[string]*PipelineItem),
	decisions: []Decision{
		{Stage: "S0-todo", Scenario: "default", ProfileTarget: "lovart-creation", Action: "upsert", Skills: []string{"lovart-pipeline-state", "lovart-blog-signal-writer"}, Reason: "S0-todo → first creation step"},
		{Stage: "S3-creating", Scenario: "default", ProfileTarget: "lovart-creation", Action: "execute_skill", Skills: []string{"lovart-blog-signal-writer"}, Reason: "Writing in progress"},
		{Stage: "S3-draft", Scenario: "default", ProfileTarget: "lovart-creation", Action: "run_hook_and_advance", Skills: []string{"post-write-check"}, Reason: "Draft exists → run post-write-check"},
		{Stage: "S3-draft", Scenario: "l1_fluff", ProfileTarget: "lovart-quality", Action: "reroute", Skills: []string{"lovart-anti-slop"}, Reason: "L1 fluff → quality profile"},
		{Stage: "S3-done", Scenario: "default", ProfileTarget: "lovart-creation", Action: "advance_only", Skills: []string{"lovart-pipeline-state"}, Reason: "S3 done → advance to S4-qa"},
		{Stage: "S4-qa", Scenario: "default", ProfileTarget: "lovart-quality", Action: "execute_skill", Skills: []string{"lovart-content-quality-gates"}, Reason: "QA in progress"},
		{Stage: "S4-fix", Scenario: "default", ProfileTarget: "lovart-creation", Action: "reroute", Skills: []string{"lovart-blog-signal-writer"}, Reason: "Fix → back to creation"},
		{Stage: "S4-ready", Scenario: "default", ProfileTarget: "lovart-quality", Action: "advance_only", Skills: []string{"lovart-pipeline-state"}, Reason: "QA done → close session"},
		{Stage: "S5-importing", Scenario: "default", ProfileTarget: "lovart-ops", Action: "execute_skill", Skills: []string{"lovart-sanity-publish", "pre-import-check"}, Reason: "Importing to Sanity"},
		{Stage: "S5-published", Scenario: "default", ProfileTarget: "lovart-ops", Action: "execute_skill", Skills: []string{"lovart-sitemap-update"}, Reason: "Notify engines"},
		{Stage: "S6-monitoring", Scenario: "default", ProfileTarget: "lovart-reports", Action: "execute_skill", Skills: []string{"lovart-seo-reporting"}, Reason: "Monitoring data"},
	},
}

// ============================================================
// API Handlers
// ============================================================

func healthHandler(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, map[string]string{"status": "ok", "time": time.Now().Format(time.RFC3339)})
}

func pipelineSummaryHandler(w http.ResponseWriter, r *http.Request) {
	store.mu.RLock()
	defer store.mu.RUnlock()
	byPhase := map[string]int{"QUEUE": 0, "CREATE": 0, "REVIEW": 0, "SHIP": 0, "FINAL": 0}
	byStage := map[string]int{}
	for _, item := range store.items {
		byPhase[item.Phase]++
		byStage[item.Stage]++
	}
	writeJSON(w, map[string]interface{}{
		"total":    len(store.items),
		"by_phase": byPhase,
		"by_stage": byStage,
	})
}

func pipelineListHandler(w http.ResponseWriter, r *http.Request) {
	store.mu.RLock()
	defer store.mu.RUnlock()
	items := make([]*PipelineItem, 0, len(store.items))
	for _, item := range store.items {
		items = append(items, item)
	}
	writeJSON(w, items)
}

func pipelineGetHandler(w http.ResponseWriter, r *http.Request) {
	id := strings.TrimPrefix(r.URL.Path, "/api/pipeline/items/")
	store.mu.RLock()
	item, ok := store.items[id]
	store.mu.RUnlock()
	if !ok {
		http.Error(w, `{"error":"not found"}`, 404)
		return
	}
	writeJSON(w, item)
}

func pipelineUpsertHandler(w http.ResponseWriter, r *http.Request) {
	var item PipelineItem
	if err := json.NewDecoder(r.Body).Decode(&item); err != nil {
		http.Error(w, `{"error":"invalid json"}`, 400)
		return
	}
	store.mu.Lock()
	defer store.mu.Unlock()
	if item.ID == "" {
		http.Error(w, `{"error":"id required"}`, 400)
		return
	}
	existing, ok := store.items[item.ID]
	if !ok {
		item.Stage = "S0-todo"
		item.Phase = "QUEUE"
		item.CreatedAt = time.Now().Format(time.RFC3339)
		item.UpdatedAt = item.CreatedAt
		item.History = []HistoryEntry{}
		store.items[item.ID] = &item
		writeJSON(w, map[string]string{"id": item.ID, "stage": item.Stage, "action": "created"})
	} else {
		if item.Category != "" { existing.Category = item.Category }
		if item.TargetType != "" { existing.TargetType = item.TargetType }
		if item.Agent != "" { existing.Agent = item.Agent }
		if item.Skill != "" { existing.Skill = item.Skill }
		if item.ArtifactPath != "" { existing.ArtifactPath = item.ArtifactPath }
		existing.UpdatedAt = time.Now().Format(time.RFC3339)
		writeJSON(w, map[string]string{"id": existing.ID, "stage": existing.Stage, "action": "updated"})
	}
}

func pipelineNextHandler(w http.ResponseWriter, r *http.Request) {
	store.mu.RLock()
	defer store.mu.RUnlock()
	for _, item := range store.items {
		if item.Stage == "S0-todo" {
			writeJSON(w, item)
			return
		}
	}
	for _, item := range store.items {
		if item.Stage == "S3-done" || item.Stage == "S4-fix" {
			writeJSON(w, item)
			return
		}
	}
	writeJSON(w, map[string]string{"status": "nothing to do"})
}

func routerDecideHandler(w http.ResponseWriter, r *http.Request) {
	var req struct {
		ID          string `json:"id"`
		FromContext string `json:"from_context"`
	}
	json.NewDecoder(r.Body).Decode(&req)

	store.mu.RLock()
	item, ok := store.items[req.ID]
	store.mu.RUnlock()

	if !ok {
		http.Error(w, `{"error":"item not found"}`, 404)
		return
	}

	// Find matching decision
	for _, d := range store.decisions {
		if d.Stage == item.Stage {
			if req.FromContext != "" && d.Scenario != "default" {
				continue // simplified: only match default for now
			}
			writeJSON(w, map[string]interface{}{
				"id":              item.ID,
				"stage":           item.Stage,
				"scenario":        d.Scenario,
				"profile_target":  d.ProfileTarget,
				"action":          d.Action,
				"skills_to_load":  d.Skills,
				"reason":          d.Reason,
			})
			return
		}
	}
	writeJSON(w, map[string]string{"status": "no decision found", "stage": item.Stage})
}

func routerMatrixHandler(w http.ResponseWriter, r *http.Request) {
	store.mu.RLock()
	defer store.mu.RUnlock()
	writeJSON(w, store.decisions)
}

func routerProfilesHandler(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, map[string]interface{}{
		"lovart-reports":      map[string]interface{}{"model": "deepseek-chat", "work_line": "S1-data + S6-monitor", "key_skills": 4},
		"lovart-creation":     map[string]interface{}{"model": "deepseek-v4-pro", "work_line": "S3-content-production", "key_skills": 5},
		"lovart-quality":      map[string]interface{}{"model": "deepseek-chat", "work_line": "S4-review", "key_skills": 4},
		"lovart-ops":          map[string]interface{}{"model": "deepseek-chat", "work_line": "S5-publish", "key_skills": 3},
		"lovart-distribution": map[string]interface{}{"model": "deepseek-chat", "work_line": "S5b-distribute", "key_skills": 2},
		"lovart-management":   map[string]interface{}{"model": "deepseek-chat", "work_line": "M0-meta", "key_skills": 4},
	})
}

func hooksRunHandler(w http.ResponseWriter, r *http.Request) {
	hookType := strings.TrimPrefix(r.URL.Path, "/api/hooks/")
	var req struct {
		File string `json:"file"`
		ID   string `json:"id"`
	}
	json.NewDecoder(r.Body).Decode(&req)

	hookDir := "/workspace/hooks"
	var cmd *exec.Cmd
	switch hookType {
	case "pre-write":
		cmd = exec.Command("bash", filepath.Join(hookDir, "pre-write-check.sh"), "--file", req.File)
	case "post-write":
		cmd = exec.Command("bash", filepath.Join(hookDir, "post-write-check.sh"), "--file", req.File, "--type", "blog", "--lang", "en", "--target-words", "7500")
	case "pre-import":
		cmd = exec.Command("bash", filepath.Join(hookDir, "pre-import-check.sh"), "--id", req.ID, "--state-path", "/workspace/scripts/pipeline-state.json", "--artifact", req.File)
	case "post-generation":
		cmd = exec.Command("bash", filepath.Join(hookDir, "post-generation-check.sh"), "--file", req.File, "--type", "blog", "--target-words", "7500")
	default:
		http.Error(w, `{"error":"unknown hook type"}`, 400)
		return
	}

	out, err := cmd.CombinedOutput()
	exitCode := 0
	if err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			exitCode = exitErr.ExitCode()
		} else {
			exitCode = 2
		}
	}

	writeJSON(w, map[string]interface{}{
		"hook":       hookType,
		"exit_code":  exitCode,
		"status":     map[int]string{0: "PASS", 1: "BLOCK", 2: "ERROR"}[exitCode],
		"output":     string(out),
	})
}

func execHandler(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Cmd string `json:"cmd"`
	}
	json.NewDecoder(r.Body).Decode(&req)
	if req.Cmd == "" {
		http.Error(w, `{"error":"cmd required"}`, 400)
		return
	}
	cmd := exec.Command("bash", "-c", req.Cmd)
	out, err := cmd.CombinedOutput()
	exitCode := 0
	if err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			exitCode = exitErr.ExitCode()
		} else {
			exitCode = 1
		}
	}
	writeJSON(w, map[string]interface{}{
		"exit_code": exitCode,
		"output":    string(out),
	})
}

// ============================================================
// Helpers
// ============================================================

func writeJSON(w http.ResponseWriter, v interface{}) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	json.NewEncoder(w).Encode(v)
}

// ============================================================
// Main
// ============================================================

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "30000"
	}

	// Health
	http.HandleFunc("/health", healthHandler)

	// Pipeline
	http.HandleFunc("/api/pipeline/summary", pipelineSummaryHandler)
	http.HandleFunc("/api/pipeline/items", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == "POST" { pipelineUpsertHandler(w, r) } else { pipelineListHandler(w, r) }
	})
	http.HandleFunc("/api/pipeline/items/", pipelineGetHandler)
	http.HandleFunc("/api/pipeline/next", pipelineNextHandler)

	// Router
	http.HandleFunc("/api/router/decide", routerDecideHandler)
	http.HandleFunc("/api/router/matrix", routerMatrixHandler)
	http.HandleFunc("/api/router/profiles", routerProfilesHandler)

	// Hooks
	http.HandleFunc("/api/hooks/", hooksRunHandler)

	// Exec (for Python scripts, skills, etc.)
	http.HandleFunc("/api/exec", execHandler)

	// Dashboard
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			http.NotFound(w, r)
			return
		}
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		w.Write([]byte(dashboardHTML))
	})

	log.Printf("Lovart MFlow API listening on :%s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}

const dashboardHTML = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Lovart MFlow Dashboard</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, sans-serif; background: #0f0f0f; color: #e0e0e0; padding: 24px; }
h1 { font-size: 24px; margin-bottom: 24px; color: #fff; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 32px; }
.card { background: #1a1a1a; border: 1px solid #333; border-radius: 8px; padding: 16px; }
.card h3 { font-size: 14px; color: #888; margin-bottom: 8px; }
.card .num { font-size: 32px; font-weight: bold; color: #4ade80; }
table { width: 100%; border-collapse: collapse; margin-top: 16px; }
th, td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #333; font-size: 14px; }
th { color: #888; }
.stage { padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.stage-queue { background: #1e3a5f; }
.stage-create { background: #1a3a1a; }
.stage-review { background: #3a3a1a; }
.stage-ship { background: #3a1a1a; }
.stage-final { background: #1a1a1a; }
</style>
</head>
<body>
<h1>Lovart MFlow Dashboard</h1>
<div class="cards" id="summary"></div>
<h2>Pipeline Items</h2>
<table><thead><tr><th>ID</th><th>Stage</th><th>Phase</th><th>Agent</th><th>Updated</th></tr></thead><tbody id="items"></tbody></table>
<script>
fetch('/api/pipeline/summary').then(r=>r.json()).then(d=>{
  const el=document.getElementById('summary');
  el.innerHTML=Object.entries(d.by_phase).map(([k,v])=>
    '<div class="card"><h3>'+k+'</h3><div class="num">'+v+'</div></div>'
  ).join('');
});
fetch('/api/pipeline/items').then(r=>r.json()).then(items=>{
  const el=document.getElementById('items');
  el.innerHTML=items.map(i=>
    '<tr><td>'+i.id+'</td><td><span class="stage stage-'+(i.phase||'').toLowerCase()+'">'+i.stage+'</span></td><td>'+i.phase+'</td><td>'+(i.agent||'-')+'</td><td>'+(i.updated_at||'-')+'</td></tr>'
  ).join('');
});
</script>
</body>
</html>`
