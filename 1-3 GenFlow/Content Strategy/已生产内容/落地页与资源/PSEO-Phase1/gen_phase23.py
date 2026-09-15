#!/usr/bin/env python3
"""Generate Phase 2+3 pages from JSON data using generate.py templates."""
import importlib.util, os, json, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# Import generator (one-time cost ~30s)
spec = importlib.util.spec_from_file_location("gen", os.path.join(BASE, "generate.py"))
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

def gen_batch(phase_dir, template_func, json_file, subdir):
    """Generate pages from JSON data using template function."""
    dst = os.path.join(BASE, phase_dir, subdir)
    os.makedirs(dst, exist_ok=True)
    
    with open(os.path.join(BASE, json_file)) as f:
        data = json.load(f)
    
    count = 0
    for entry in data:
        path = os.path.join(dst, f"{entry['slug']}.md")
        if os.path.exists(path):
            continue  # skip existing
        content = template_func(entry)
        with open(path, 'w') as f:
            f.write(content)
        count += 1
    return count

# Generate all Phase 2 batches
print("=== Phase 2 ===")
for batch in [
    ("PSEO-Phase2", "p2_t2.json", "T2-Chat-Generate"),
    ("PSEO-Phase2", "p2_t3.json", "T3-No-Photoshop"),
    ("PSEO-Phase2", "p2_t4.json", "T4-Brand-Kit"),
]:
    func = getattr(gen, f"gen_{batch[2][:2].lower()}")
    n = gen_batch(batch[0], func, batch[1], batch[2])
    print(f"  {batch[2]}: {n} pages")

# Generate all Phase 3 batches
print("\n=== Phase 3 ===")
for batch in [
    ("PSEO-Phase3", "p3_t1.json", "T1-Best-Agent"),
    ("PSEO-Phase3", "p3_t2.json", "T2-Chat-Generate"),
    ("PSEO-Phase3", "p3_t3.json", "T3-No-Photoshop"),
    ("PSEO-Phase3", "p3_t4.json", "T4-Brand-Kit"),
]:
    func = getattr(gen, f"gen_{batch[2][:2].lower()}")
    n = gen_batch(batch[0], func, batch[1], batch[2])
    print(f"  {batch[2]}: {n} pages")

# Summary
for phase in ["PSEO-Phase2", "PSEO-Phase3"]:
    phase_dir = os.path.join(BASE, phase)
    if not os.path.exists(phase_dir):
        continue
    all_f = glob.glob(f"{phase_dir}/**/*.md", recursive=True)
    if all_f:
        total_w = sum(len(open(f).read().split()) for f in all_f)
        print(f"\n{phase}: {len(all_f)} pages, ~{total_w} words, avg ~{total_w//len(all_f)}")
