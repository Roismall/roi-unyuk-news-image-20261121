// News-image entry (Node 22, standard library only).
//
// The front page for Saturday 21 November 2026 is rendered ahead of time
// by render.py and held in this repository as entry.png. The program's
// only job is to copy that image to the grader's output directory, so
// both runs write byte-identical output with no network access.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = new URL("./entry.png", import.meta.url);

copyFileSync(source, join(outDir, "entry.png"));
