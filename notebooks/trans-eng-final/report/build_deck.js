// Build the trans-eng final project presentation.
// Theme ported from AI-Mobility-Audit-Framework/assignments/research-methods-class/build_deck.js

const pptxgen = require("pptxgenjs");
const path = require("path");

const BASE = path.resolve(__dirname);
const FIG = path.join(BASE, "..", "figures");
const OUT = path.join(BASE, "trans-eng-presentation.pptx");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3" x 7.5"
pres.author = "Dhaneswara Mandrasa Triweko";
pres.title = "Mode Choice and Policy Welfare in Jabodetabek";

// ---------------- Palette ----------------
const NAVY = "1E2761";
const NAVY_DEEP = "151B3F";
const TEAL = "028090";
const TEAL_SOFT = "00A896";
const CREAM = "F7F5EF";
const PAPER = "FFFFFF";
const INK = "1A1A1A";
const MUTE = "5C6677";
const RULE = "D8DCE3";
const HIGHLIGHT = "F2D27B";
const WARM = "C2474C";

const HEAD_FONT = "Georgia";
const BODY_FONT = "Calibri";
const MONO_FONT = "Consolas";

const TOTAL = 15;

// ---------------- Reusable elements ----------------
function addFooter(slide, pageNum) {
  slide.addShape(pres.shapes.LINE, {
    x: 0.6, y: 7.05, w: 12.1, h: 0,
    line: { color: RULE, width: 0.75 },
  });
  slide.addText("Dhaneswaramandrasa  ·  Transportation Engineering  ·  Hiroshima University AY2026", {
    x: 0.6, y: 7.12, w: 9, h: 0.3,
    fontFace: BODY_FONT, fontSize: 9, color: MUTE, margin: 0,
  });
  slide.addText(`${pageNum} / ${TOTAL}`, {
    x: 11.5, y: 7.12, w: 1.2, h: 0.3,
    fontFace: BODY_FONT, fontSize: 9, color: MUTE, align: "right", margin: 0,
  });
}

function sectionTag(slide, label) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 0.55, w: 0.12, h: 0.32,
    fill: { color: TEAL }, line: { color: TEAL, width: 0 },
  });
  slide.addText(label.toUpperCase(), {
    x: 0.85, y: 0.55, w: 8, h: 0.32,
    fontFace: BODY_FONT, fontSize: 11, bold: true, color: TEAL,
    charSpacing: 4, margin: 0, valign: "middle",
  });
}

function slideTitle(slide, title) {
  slide.addText(title, {
    x: 0.6, y: 0.95, w: 12.1, h: 0.75,
    fontFace: HEAD_FONT, fontSize: 28, bold: true, color: NAVY,
    margin: 0,
  });
}

// =====================================================
// SLIDE 1 — Title
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: NAVY_DEEP };

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.35, h: 7.5,
    fill: { color: TEAL }, line: { color: TEAL, width: 0 },
  });

  s.addText("TRANSPORTATION ENGINEERING  ·  FINAL PROJECT", {
    x: 0.9, y: 1.4, w: 11, h: 0.3,
    fontFace: BODY_FONT, fontSize: 12, color: TEAL_SOFT, bold: true,
    charSpacing: 6, margin: 0,
  });

  s.addText([
    { text: "Mode Choice and Policy Welfare", options: { breakLine: true } },
    { text: "in Jabodetabek", options: { breakLine: true } },
  ], {
    x: 0.9, y: 1.95, w: 11.5, h: 2.0,
    fontFace: HEAD_FONT, fontSize: 36, bold: true, color: PAPER,
    margin: 0,
  });

  s.addText("An MNL → Nested Logit → Mixed Logit Comparison", {
    x: 0.9, y: 3.85, w: 11, h: 0.55,
    fontFace: HEAD_FONT, fontSize: 18, italic: true, color: "CADCFC",
    margin: 0,
  });

  s.addShape(pres.shapes.LINE, {
    x: 0.9, y: 5.0, w: 3.0, h: 0,
    line: { color: TEAL, width: 1.5 },
  });
  s.addText([
    { text: "Dhaneswaramandrasa", options: { bold: true, color: PAPER, fontSize: 16, breakLine: true } },
    { text: "Hiroshima University · Transportation Engineering AY2026", options: { color: "CADCFC", fontSize: 12, breakLine: true } },
    { text: "Session L15 · June 3, 2026", options: { color: "CADCFC", fontSize: 12 } },
  ], {
    x: 0.9, y: 5.15, w: 8, h: 1.3,
    fontFace: BODY_FONT, margin: 0,
  });
}

// =====================================================
// SLIDE 2 — Motivation
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: CREAM };
  sectionTag(s, "01  ·  motivation");
  slideTitle(s, "Why Jabodetabek mode choice matters");

  const cards = [
    {
      title: "30M+ population",
      sub: "SCALE",
      body: "3.5 million daily commuters. Car/motorcycle-dominated mode split despite massive transit investment.",
    },
    {
      title: "Spatial inequality",
      sub: "COVERAGE GAP",
      body: "Transit expansion is spatially uneven: J1b (Parung) and J3b (Gading Serpong) have no formal transit at all.",
    },
    {
      title: "Policy question",
      sub: "WELFARE",
      body: "Which policies maximize welfare? How are gains distributed across zones and income segments?",
    },
  ];

  const cardW = 3.97;
  const gap = 0.20;
  const startX = 0.6;
  cards.forEach((c, i) => {
    const x = startX + i * (cardW + gap);
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.85, w: cardW, h: 3.2,
      fill: { color: PAPER }, line: { color: RULE, width: 0.75 },
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.85, w: cardW, h: 0.08,
      fill: { color: NAVY }, line: { color: NAVY, width: 0 },
    });
    s.addText(c.sub, {
      x: x + 0.25, y: 2.05, w: cardW - 0.4, h: 0.3,
      fontFace: BODY_FONT, fontSize: 10, color: TEAL, bold: true, charSpacing: 3, margin: 0,
    });
    s.addText(c.title, {
      x: x + 0.25, y: 2.35, w: cardW - 0.4, h: 0.5,
      fontFace: HEAD_FONT, fontSize: 20, bold: true, color: NAVY, margin: 0,
    });
    s.addShape(pres.shapes.LINE, {
      x: x + 0.25, y: 2.95, w: 0.6, h: 0,
      line: { color: TEAL, width: 1.5 },
    });
    s.addText(c.body, {
      x: x + 0.25, y: 3.15, w: cardW - 0.5, h: 1.7,
      fontFace: BODY_FONT, fontSize: 13, color: INK, margin: 0,
    });
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 5.30, w: 12.1, h: 0.85,
    fill: { color: NAVY }, line: { color: NAVY, width: 0 },
  });
  s.addText([
    { text: "Framework:  ", options: { bold: true, color: HIGHLIGHT } },
    { text: "6-mode choice set → MNL / NL / MXL → AIC / LR / Wald selection → logsum ΔCS → 8 policy scenarios", options: { color: PAPER } },
  ], {
    x: 0.9, y: 5.30, w: 11.5, h: 0.85,
    fontFace: BODY_FONT, fontSize: 13, valign: "middle", margin: 0,
  });

  addFooter(s, 2);
}

// =====================================================
// SLIDE 3 — Study Area & Data
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  sectionTag(s, "02  ·  study area & data");
  slideTitle(s, "Seven zones, six modes, synthetic population");

  const rows = [
    ["Zones (7)", "J1a–J5, Bodetabek → Jakarta CBD"],
    ["Modes (6)", "Car, Motorcycle, KRL, TransJakarta, RoyalTrans, MRT"],
    ["Nest structure", "Transit {KRL, MRT, TJ, Royal} · Private {Car, Moto}"],
    ["Population", "5,000 synthetic persons; 3 income segments (BPS Susenas 2023)"],
    ["Transit LOS", "r5py GTFS routing (AM peak 07:00–09:00, fallback 180 min)"],
    ["Private LOS", "BPR free-flow speeds (toll 80, arterial 40, local 25 km/h)"],
    ["DGP", "NL GEV closed-form choice generation, μ=25 scale normalization"],
  ];

  const tableX = 0.6;
  const tableY = 1.85;
  const colW = [2.4, 9.7];
  const rowH = 0.55;

  rows.forEach((row, i) => {
    const y = tableY + i * rowH;
    const bg = i % 2 === 0 ? CREAM : PAPER;
    s.addShape(pres.shapes.RECTANGLE, {
      x: tableX, y, w: colW[0] + colW[1], h: rowH,
      fill: { color: bg }, line: { color: RULE, width: 0.5 },
    });
    s.addText(row[0], {
      x: tableX + 0.15, y, w: colW[0] - 0.3, h: rowH,
      fontFace: BODY_FONT, fontSize: 12, bold: true, color: NAVY, valign: "middle", margin: 0,
    });
    s.addText(row[1], {
      x: tableX + colW[0] + 0.15, y, w: colW[1] - 0.3, h: rowH,
      fontFace: BODY_FONT, fontSize: 12, color: INK, valign: "middle", margin: 0,
    });
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 5.85, w: 12.1, h: 1.0,
    fill: { color: NAVY }, line: { color: NAVY, width: 0 },
  });
  s.addText([
    { text: "β calibration:  ", options: { bold: true, color: HIGHLIGHT } },
    { text: "β_time,m derived from Ilahi et al. (2021) Table 11 mode-specific VTTS via β_time = β_cost · VTTS / 60,000. β_cost = −1.42. VOT preserved exactly under μ=25 scale normalization (Train 2009 §3.7).", options: { color: PAPER } },
  ], {
    x: 0.9, y: 5.85, w: 11.5, h: 1.0,
    fontFace: BODY_FONT, fontSize: 11, valign: "middle", margin: 0,
  });

  addFooter(s, 3);
}

// =====================================================
// SLIDE 4 — MNL Specification
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: CREAM };
  sectionTag(s, "03  ·  mnl estimation");
  slideTitle(s, "MNL: specification & IIA problem");

  s.addText("Vₘₙ = ASCₘ + β_time,m · Tₖₙ + β_cost · Cₖₙ", {
    x: 0.6, y: 1.85, w: 12.1, h: 0.6,
    fontFace: MONO_FONT, fontSize: 18, color: NAVY, margin: 0,
  });

  s.addText("12 parameters  ·  L-BFGS-B MLE  ·  KRL = reference alternative", {
    x: 0.6, y: 2.45, w: 12.1, h: 0.35,
    fontFace: BODY_FONT, fontSize: 13, italic: true, color: MUTE, margin: 0,
  });

  // Results cards
  const left = [
    { lbl: "Parameter recovery", val: "12/12 within 2 SE" },
    { lbl: "ρ²", val: "0.280" },
    { lbl: "AIC", val: "10,121.65" },
  ];

  left.forEach((r, i) => {
    const y = 3.0 + i * 0.7;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.6, y, w: 5.5, h: 0.6,
      fill: { color: PAPER }, line: { color: RULE, width: 0.5 },
    });
    s.addText(r.lbl, {
      x: 0.8, y, w: 3.0, h: 0.6,
      fontFace: BODY_FONT, fontSize: 13, bold: true, color: NAVY, valign: "middle", margin: 0,
    });
    s.addText(r.val, {
      x: 3.8, y, w: 2.2, h: 0.6,
      fontFace: MONO_FONT, fontSize: 14, color: TEAL, bold: true, valign: "middle", align: "right", margin: [0, 10, 0, 0],
    });
  });

  // IIA violation box
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.5, y: 3.0, w: 6.2, h: 2.1,
    fill: { color: PAPER }, line: { color: WARM, width: 1.5 },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.5, y: 3.0, w: 6.2, h: 0.08,
    fill: { color: WARM }, line: { color: WARM, width: 0 },
  });
  s.addText("IIA IS VIOLATED", {
    x: 6.75, y: 3.15, w: 5.5, h: 0.3,
    fontFace: BODY_FONT, fontSize: 10, bold: true, color: WARM, charSpacing: 3, margin: 0,
  });
  s.addText([
    { text: "Red-bus/blue-bus: ", options: { bold: true } },
    { text: "clone KRL as \"KRL Express\" → transit share nearly doubles (11.7% → 21.8%)", options: { breakLine: true } },
    { text: "\n" },
    { text: "NL cross-elasticity: ", options: { bold: true } },
    { text: "within-nest substitution 1.67× cross-nest. MNL forces equal proportional substitution.", options: {} },
  ], {
    x: 6.75, y: 3.50, w: 5.7, h: 1.5,
    fontFace: BODY_FONT, fontSize: 12, color: INK, margin: 0,
  });

  s.addText("MNL fails to capture the correlation among transit alternatives → need Nested Logit.", {
    x: 0.6, y: 5.5, w: 12.1, h: 0.35,
    fontFace: BODY_FONT, fontSize: 13, italic: true, color: MUTE, align: "center", margin: 0,
  });

  addFooter(s, 4);
}

// =====================================================
// SLIDE 5 — Nested Logit
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  sectionTag(s, "04  ·  nested logit");
  slideTitle(s, "NL: λ̂ = 0.763 — nesting confirmed");

  s.addText("Pₙ(m) = Pₙ(m|k) · Pₙ(k),    Pₙ(k) = exp(λ Iₖₙ) / Σₗ exp(λ Iₗₙ)", {
    x: 0.6, y: 1.85, w: 12.1, h: 0.55,
    fontFace: MONO_FONT, fontSize: 16, color: NAVY, margin: 0,
  });

  s.addText("Two nests  ·  13 parameters  ·  FIML via L-BFGS-B", {
    x: 0.6, y: 2.40, w: 12.1, h: 0.35,
    fontFace: BODY_FONT, fontSize: 13, italic: true, color: MUTE, margin: 0,
  });

  const params = [
    ["λ̂", "0.763 ± 0.068"],
    ["95% CI", "[0.627, 0.900] — excludes 1.0"],
    ["LR test vs MNL", "χ² = 8.57, df = 1, p = 0.003"],
    ["Recovery", "13/13 within 2 SE"],
    ["AIC / BIC", "10,115.08 / 10,199.80"],
  ];

  params.forEach((row, i) => {
    const y = 2.95 + i * 0.58;
    const bg = i % 2 === 0 ? CREAM : PAPER;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.6, y, w: 7.5, h: 0.5,
      fill: { color: bg }, line: { color: RULE, width: 0.5 },
    });
    s.addText(row[0], {
      x: 0.8, y, w: 3.0, h: 0.5,
      fontFace: BODY_FONT, fontSize: 13, bold: true, color: NAVY, valign: "middle", margin: 0,
    });
    s.addText(row[1], {
      x: 3.8, y, w: 4.1, h: 0.5,
      fontFace: MONO_FONT, fontSize: 13, color: INK, valign: "middle", margin: 0,
    });
  });

  // Interpretation box
  s.addShape(pres.shapes.RECTANGLE, {
    x: 8.5, y: 2.95, w: 4.2, h: 2.9,
    fill: { color: NAVY }, line: { color: NAVY, width: 0 },
  });
  s.addText("KEY FINDING", {
    x: 8.75, y: 3.10, w: 3.7, h: 0.3,
    fontFace: BODY_FONT, fontSize: 10, bold: true, color: HIGHLIGHT, charSpacing: 3, margin: 0,
  });
  s.addText("λ = 1 rejected at p < 0.01", {
    x: 8.75, y: 3.45, w: 3.7, h: 0.55,
    fontFace: HEAD_FONT, fontSize: 17, bold: true, color: PAPER, margin: 0,
  });
  s.addText("Transit modes share unobserved attributes (crowding, schedule coordination, station environment) that make them closer substitutes than IIA allows.", {
    x: 8.75, y: 4.05, w: 3.7, h: 1.7,
    fontFace: BODY_FONT, fontSize: 12, color: "CADCFC", margin: 0,
  });

  addFooter(s, 5);
}

// =====================================================
// SLIDE 6 — Mixed Logit
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: CREAM };
  sectionTag(s, "05  ·  mixed logit");
  slideTitle(s, "MXL: σ̂ = 0.010 — no taste heterogeneity");

  s.addText("Random β_cost ~ N(μ, σ)  ·  R = 100 Halton draws (base=2)", {
    x: 0.6, y: 1.85, w: 12.1, h: 0.4,
    fontFace: BODY_FONT, fontSize: 13, italic: true, color: MUTE, margin: 0,
  });

  s.addText("H₀: σ_cost = 0 — any heterogeneity beyond NL nest correlation?", {
    x: 0.6, y: 2.25, w: 12.1, h: 0.4,
    fontFace: BODY_FONT, fontSize: 14, bold: true, color: NAVY, margin: 0,
  });

  // Results
  const mxlResults = [
    ["σ_cost", "0.010", "0.033"],
    ["μ_cost", "−0.037", "0.183"],
  ];

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 2.85, w: 6.0, h: 0.45,
    fill: { color: NAVY }, line: { color: NAVY, width: 0 },
  });
  ["Parameter", "Estimate", "SE"].forEach((h, i) => {
    s.addText(h, {
      x: 0.6 + i * 2.0, y: 2.85, w: 2.0, h: 0.45,
      fontFace: BODY_FONT, fontSize: 12, bold: true, color: PAPER, valign: "middle", margin: [0, 0, 0, 15],
    });
  });

  mxlResults.forEach((row, i) => {
    const y = 3.30 + i * 0.5;
    const bg = i % 2 === 0 ? PAPER : CREAM;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.6, y, w: 6.0, h: 0.5,
      fill: { color: bg }, line: { color: RULE, width: 0.5 },
    });
    row.forEach((cell, j) => {
      s.addText(cell, {
        x: 0.6 + j * 2.0, y, w: 2.0, h: 0.5,
        fontFace: j === 0 ? BODY_FONT : MONO_FONT, fontSize: 13,
        bold: j === 0, color: j === 0 ? NAVY : INK,
        valign: "middle", margin: [0, 0, 0, 15],
      });
    });
  });

  // Wald test
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 4.5, w: 6.0, h: 0.6,
    fill: { color: PAPER }, line: { color: TEAL, width: 1.5 },
  });
  s.addText([
    { text: "Wald:  ", options: { bold: true, color: NAVY } },
    { text: "W = 0.091,  p = 0.763  →  fail to reject H₀", options: { color: INK } },
  ], {
    x: 0.8, y: 4.5, w: 5.6, h: 0.6,
    fontFace: BODY_FONT, fontSize: 13, valign: "middle", margin: 0,
  });

  // Right column: interpretation
  s.addShape(pres.shapes.RECTANGLE, {
    x: 7.0, y: 2.85, w: 5.7, h: 2.25,
    fill: { color: PAPER }, line: { color: RULE, width: 0.75 },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 7.0, y: 2.85, w: 0.08, h: 2.25,
    fill: { color: TEAL }, line: { color: TEAL, width: 0 },
  });

  const interp = [
    { text: "Positive control: ", options: { bold: true } },
    { text: "Mixed-DGP (σ_true=0.02) → Wald p ≈ 0 ✓", options: { breakLine: true } },
    { text: "\n" },
    { text: "Finding: ", options: { bold: true } },
    { text: "No taste heterogeneity signal. MXL LL (−5,048.79) ≈ MNL LL (−5,048.83). Adding random β_cost gains 0.03 LL units — negligible.", options: { breakLine: true } },
    { text: "\n" },
    { text: "NL captures the departure from IIA that matters.", options: { bold: true, color: TEAL } },
  ];
  s.addText(interp, {
    x: 7.25, y: 2.95, w: 5.2, h: 2.05,
    fontFace: BODY_FONT, fontSize: 12, color: INK, margin: 0,
  });

  addFooter(s, 6);
}

// =====================================================
// SLIDE 7 — Model Selection
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  sectionTag(s, "06  ·  model selection");
  slideTitle(s, "NL wins on every criterion");

  const headers = ["Criterion", "MNL", "NL", "MXL"];
  const colWidths = [3.0, 2.5, 2.8, 2.8];
  const tableX = 0.6;
  const startY = 2.0;

  // Header row
  s.addShape(pres.shapes.RECTANGLE, {
    x: tableX, y: startY, w: 11.1, h: 0.55,
    fill: { color: NAVY }, line: { color: NAVY, width: 0 },
  });
  let cx = tableX;
  headers.forEach((h, i) => {
    s.addText(h, {
      x: cx, y: startY, w: colWidths[i], h: 0.55,
      fontFace: BODY_FONT, fontSize: 13, bold: true, color: PAPER, valign: "middle", margin: [0, 0, 0, 15],
    });
    cx += colWidths[i];
  });

  const tableData = [
    ["K", "12", "13", "13"],
    ["LL(β̂)", "−5,048.83", "−5,044.54", "−5,048.79"],
    ["AIC", "10,121.65", "10,115.08", "10,123.59"],
    ["BIC", "10,199.86", "10,199.80", "10,208.31"],
    ["LR vs MNL (p)", "—", "0.003", "0.799"],
    ["Wald σ=0 (p)", "—", "—", "0.763"],
  ];

  tableData.forEach((row, i) => {
    const y = startY + 0.55 + i * 0.5;
    const bg = i % 2 === 0 ? CREAM : PAPER;
    s.addShape(pres.shapes.RECTANGLE, {
      x: tableX, y, w: 11.1, h: 0.5,
      fill: { color: bg }, line: { color: RULE, width: 0.5 },
    });
    let rx = tableX;
    row.forEach((cell, j) => {
      const isNL = j === 2;
      s.addText(cell, {
        x: rx, y, w: colWidths[j], h: 0.5,
        fontFace: j === 0 ? BODY_FONT : MONO_FONT,
        fontSize: 13,
        bold: j === 0 || isNL,
        color: isNL ? TEAL : (j === 0 ? NAVY : INK),
        valign: "middle",
        margin: [0, 0, 0, 15],
      });
      rx += colWidths[j];
    });
  });

  // Bottom summary
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 5.65, w: 12.1, h: 0.85,
    fill: { color: NAVY }, line: { color: NAVY, width: 0 },
  });
  s.addText([
    { text: "NL selected:  ", options: { bold: true, color: HIGHLIGHT } },
    { text: "ΔAIC = −6.6 vs MNL, −8.5 vs MXL. LR rejects IIA at p<0.01. Wald fails to reject σ=0. Parsimonious correct specification → best_model.json", options: { color: PAPER } },
  ], {
    x: 0.9, y: 5.65, w: 11.5, h: 0.85,
    fontFace: BODY_FONT, fontSize: 13, valign: "middle", margin: 0,
  });

  addFooter(s, 7);
}

// =====================================================
// SLIDE 8 — Logsum Welfare Measurement
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: CREAM };
  sectionTag(s, "07  ·  welfare measurement");
  slideTitle(s, "Logsum consumer surplus from NL");

  const eqs = [
    "EMUₙ = ln Σₖ exp(λ · Iₖₙ),    Iₖₙ = ln Σⱼ∈ₖ exp(Vⱼₙ / λ)",
    "CSₙ = EMUₙ / |β_cost|,    ΔCSₙ = (EMU^policy − EMU^baseline) / |β_cost|",
    "ΔW_annual = Σₙ ΔCSₙ × 250",
  ];

  eqs.forEach((eq, i) => {
    s.addText(eq, {
      x: 0.6, y: 1.95 + i * 0.55, w: 12.1, h: 0.5,
      fontFace: MONO_FONT, fontSize: 14, color: NAVY, margin: 0,
    });
  });

  // Baseline cards
  const baseCards = [
    { lbl: "Baseline CS", val: "−53.65", unit: "Th IDR/trip" },
    { lbl: "P10", val: "−115.30", unit: "Th IDR/trip" },
    { lbl: "P90", val: "−9.48", unit: "Th IDR/trip" },
    { lbl: "β_cost (NL)", val: "−0.077", unit: "SE = 0.097" },
  ];

  baseCards.forEach((c, i) => {
    const x = 0.6 + i * 3.1;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 3.75, w: 2.9, h: 1.5,
      fill: { color: PAPER }, line: { color: RULE, width: 0.75 },
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 3.75, w: 2.9, h: 0.08,
      fill: { color: TEAL }, line: { color: TEAL, width: 0 },
    });
    s.addText(c.lbl, {
      x: x + 0.15, y: 3.90, w: 2.6, h: 0.3,
      fontFace: BODY_FONT, fontSize: 10, bold: true, color: TEAL, charSpacing: 2, margin: 0,
    });
    s.addText(c.val, {
      x: x + 0.15, y: 4.25, w: 2.6, h: 0.55,
      fontFace: HEAD_FONT, fontSize: 26, bold: true, color: NAVY, margin: 0,
    });
    s.addText(c.unit, {
      x: x + 0.15, y: 4.80, w: 2.6, h: 0.35,
      fontFace: BODY_FONT, fontSize: 11, color: MUTE, margin: 0,
    });
  });

  s.addText("Bootstrap CIs use truncated-Normal draws (upper bound = −0.3·|β̂|) to bound welfare estimates.", {
    x: 0.6, y: 5.55, w: 12.1, h: 0.35,
    fontFace: BODY_FONT, fontSize: 12, italic: true, color: MUTE, align: "center", margin: 0,
  });

  addFooter(s, 8);
}

// =====================================================
// SLIDE 9 — Policy Scenarios Overview
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  sectionTag(s, "08  ·  policy scenarios");
  slideTitle(s, "Eight scenarios — aggregate ΔCS comparison");

  s.addImage({
    path: path.join(FIG, "fig04_scenario_comparison.png"),
    x: 0.6, y: 1.95, w: 12.1, h: 4.0,
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 6.15, w: 12.1, h: 0.85,
    fill: { color: NAVY }, line: { color: NAVY, width: 0 },
  });
  s.addText([
    { text: "Top 3 by ΔCS:  ", options: { bold: true, color: HIGHLIGHT } },
    { text: "C (KRL freq, +3.76) > D (TJ→J1b, +3.29) > H (RT fare, +1.99).  ", options: { color: PAPER } },
    { text: "Regressive:  ", options: { bold: true, color: HIGHLIGHT } },
    { text: "B (toll, −0.10, 0 winners)", options: { color: PAPER } },
  ], {
    x: 0.9, y: 6.15, w: 11.5, h: 0.85,
    fontFace: BODY_FONT, fontSize: 13, valign: "middle", margin: 0,
  });

  addFooter(s, 9);
}

// =====================================================
// SLIDE 10 — Distributional Impact
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: CREAM };
  sectionTag(s, "09  ·  distributional impact");
  slideTitle(s, "Who wins and who is left out?");

  s.addImage({
    path: path.join(FIG, "fig04_dcs_heatmap.png"),
    x: 0.6, y: 1.95, w: 7.5, h: 4.2,
  });

  // Right column: insight cards
  const insights = [
    {
      tag: "SC C",
      text: "Maximizes aggregate welfare but J1b/J3b receive zero — no rail access.",
      color: TEAL,
    },
    {
      tag: "SC D",
      text: "Concentrates gains in transit-orphan J1b (+28.43 Th IDR). TJ draws from motorcycles (−10.1 pp), not other transit.",
      color: NAVY,
    },
    {
      tag: "SC F",
      text: "Benefits both J3a (+9.66) and J3b (+2.49) through TJ BSD→CBD route restructuring.",
      color: TEAL,
    },
  ];

  insights.forEach((ins, i) => {
    const y = 1.95 + i * 1.45;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 8.5, y, w: 4.2, h: 1.3,
      fill: { color: PAPER }, line: { color: RULE, width: 0.75 },
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: 8.5, y, w: 0.08, h: 1.3,
      fill: { color: ins.color }, line: { color: ins.color, width: 0 },
    });
    s.addText(ins.tag, {
      x: 8.75, y: y + 0.1, w: 3.7, h: 0.3,
      fontFace: BODY_FONT, fontSize: 10, bold: true, color: ins.color, charSpacing: 3, margin: 0,
    });
    s.addText(ins.text, {
      x: 8.75, y: y + 0.4, w: 3.7, h: 0.8,
      fontFace: BODY_FONT, fontSize: 11, color: INK, margin: 0,
    });
  });

  addFooter(s, 10);
}

// =====================================================
// SLIDE 11 — Mode Shifts
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  sectionTag(s, "10  ·  mode shifts");
  slideTitle(s, "Where do new riders come from?");

  s.addImage({
    path: path.join(FIG, "fig04_mode_shifts.png"),
    x: 0.6, y: 1.95, w: 12.1, h: 4.2,
  });

  s.addText("Budget transit (TJ at Rp 3,500) draws primarily from motorcycles, not from other transit modes — expanding the pie rather than reshuffling it.", {
    x: 0.6, y: 6.35, w: 12.1, h: 0.45,
    fontFace: BODY_FONT, fontSize: 13, italic: true, color: MUTE, align: "center", margin: 0,
  });

  addFooter(s, 11);
}

// =====================================================
// SLIDE 12 — Conclusions
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: CREAM };
  sectionTag(s, "11  ·  conclusions");
  slideTitle(s, "Four takeaways");

  const conclusions = [
    {
      num: "1",
      title: "NL is the appropriate model",
      body: "λ̂ = 0.763, LR p = 0.003, MXL adds no signal (Wald p = 0.763)",
    },
    {
      num: "2",
      title: "Top aggregate gain: Sc C",
      body: "KRL frequency improvement: +3.76 Th IDR/trip, +6,580 Bn IDR/year",
    },
    {
      num: "3",
      title: "Most pro-equity: Sc D",
      body: "TJ extension to J1b: +3.29 Th IDR/trip — concentrated in the most underserved zone",
    },
    {
      num: "4",
      title: "Bundle quality + expansion",
      body: "Service quality improvements alone leave transit orphans behind. Combine with network expansion for equitable gains.",
    },
  ];

  conclusions.forEach((c, i) => {
    const y = 1.95 + i * 1.2;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.6, y, w: 12.1, h: 1.05,
      fill: { color: PAPER }, line: { color: RULE, width: 0.75 },
    });
    // Number circle
    s.addShape(pres.shapes.OVAL, {
      x: 0.85, y: y + 0.2, w: 0.6, h: 0.6,
      fill: { color: NAVY }, line: { color: NAVY, width: 0 },
    });
    s.addText(c.num, {
      x: 0.85, y: y + 0.2, w: 0.6, h: 0.6,
      fontFace: HEAD_FONT, fontSize: 20, bold: true, color: PAPER, align: "center", valign: "middle", margin: 0,
    });
    s.addText(c.title, {
      x: 1.7, y: y + 0.1, w: 10.7, h: 0.45,
      fontFace: HEAD_FONT, fontSize: 17, bold: true, color: NAVY, valign: "middle", margin: 0,
    });
    s.addText(c.body, {
      x: 1.7, y: y + 0.55, w: 10.7, h: 0.45,
      fontFace: BODY_FONT, fontSize: 12, color: INK, valign: "top", margin: 0,
    });
  });

  addFooter(s, 12);
}

// =====================================================
// SLIDE 13 — Thank You
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: NAVY_DEEP };

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.35, h: 7.5,
    fill: { color: TEAL }, line: { color: TEAL, width: 0 },
  });

  s.addText("Thank You", {
    x: 0.9, y: 2.5, w: 11.5, h: 1.2,
    fontFace: HEAD_FONT, fontSize: 48, bold: true, color: PAPER, margin: 0,
  });

  s.addShape(pres.shapes.LINE, {
    x: 0.9, y: 3.8, w: 3.0, h: 0,
    line: { color: TEAL, width: 1.5 },
  });

  s.addText("Questions?", {
    x: 0.9, y: 4.0, w: 11.5, h: 0.8,
    fontFace: HEAD_FONT, fontSize: 28, italic: true, color: "CADCFC", margin: 0,
  });
}

// =====================================================
// SLIDE 14 — Backup A: Why σ = 25?
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  sectionTag(s, "backup a");
  slideTitle(s, "Why scale parameter μ = 25?");

  s.addText("Scale identification theorem (Train 2009 §3.7):", {
    x: 0.6, y: 1.85, w: 12.1, h: 0.4,
    fontFace: BODY_FONT, fontSize: 14, bold: true, color: NAVY, margin: 0,
  });

  const steps = [
    "True utility: U = V + ε, where ε ~ Gumbel(0, μ)",
    "Normalized: Ũ = Ṽ + ε̃, where ε̃ ~ Gumbel(0, 1)",
    "All coefficients compressed: β̃ = β / μ",
    "VOT = β_time / β_cost is preserved — μ cancels",
  ];

  steps.forEach((step, i) => {
    s.addText(step, {
      x: 0.85, y: 2.4 + i * 0.45, w: 11.5, h: 0.4,
      fontFace: MONO_FONT, fontSize: 13, color: INK, margin: 0,
    });
  });

  // Two-column explanation
  const cols = [
    {
      title: "Without μ = 25",
      body: "Utility gaps too large → choice becomes deterministic (99%+ choosing one mode). No meaningful choice model.",
      color: WARM,
      fill: "FFF5F5",
    },
    {
      title: "With μ = 25",
      body: "β estimates have larger SEs (the tradeoff), but Gumbel noise produces realistic choice distributions: Moto 36.7%, TJ 34.0%, KRL 17.8%.",
      color: TEAL,
      fill: CREAM,
    },
  ];

  cols.forEach((c, i) => {
    const x = 0.6 + i * 6.25;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 4.35, w: 6.0, h: 2.3,
      fill: { color: c.fill }, line: { color: c.color, width: 1.5 },
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 4.35, w: 6.0, h: 0.1,
      fill: { color: c.color }, line: { color: c.color, width: 0 },
    });
    s.addText(c.title, {
      x: x + 0.25, y: 4.55, w: 5.5, h: 0.5,
      fontFace: HEAD_FONT, fontSize: 17, bold: true, color: c.color, margin: 0,
    });
    s.addText(c.body, {
      x: x + 0.25, y: 5.1, w: 5.5, h: 1.4,
      fontFace: BODY_FONT, fontSize: 12, color: INK, margin: 0,
    });
  });

  addFooter(s, 14);
}

// =====================================================
// SLIDE 15 — Backup B: Why Drop Ride-Hailing & LRT?
// =====================================================
{
  const s = pres.addSlide();
  s.background = { color: CREAM };
  sectionTag(s, "backup b");
  slideTitle(s, "Why drop ride-hailing & LRT?");

  const modes = [
    {
      mode: "2WRH (GoRide/GrabBike)",
      reason: "Ilahi β_time_2wrh = −5.10 estimated on short urban trips → near-zero share on 30–105 km commutes. Parameter non-transferability (Wardman et al. 2016).",
    },
    {
      mode: "4WRH (GoCar/GrabCar)",
      reason: "ASC calibration required >+40 utility units to match BPS aggregate share — outside defensible range.",
    },
    {
      mode: "LRT Jabodebek",
      reason: "Available in only 1 of 7 zones (J2). Single-zone presence → ASC absorbs zone unobservables, not mode preference.",
    },
  ];

  modes.forEach((m, i) => {
    const y = 2.0 + i * 1.55;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.6, y, w: 12.1, h: 1.35,
      fill: { color: PAPER }, line: { color: RULE, width: 0.75 },
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.6, y, w: 0.08, h: 1.35,
      fill: { color: WARM }, line: { color: WARM, width: 0 },
    });
    s.addText(m.mode, {
      x: 0.85, y: y + 0.1, w: 11.5, h: 0.4,
      fontFace: HEAD_FONT, fontSize: 16, bold: true, color: NAVY, margin: 0,
    });
    s.addText(m.reason, {
      x: 0.85, y: y + 0.55, w: 11.5, h: 0.7,
      fontFace: BODY_FONT, fontSize: 12, color: INK, margin: 0,
    });
  });

  s.addText("Nine-mode DGP tested → six-mode adopted. Documented in report §2.2, §6.3.", {
    x: 0.6, y: 6.55, w: 12.1, h: 0.35,
    fontFace: BODY_FONT, fontSize: 12, italic: true, color: MUTE, align: "center", margin: 0,
  });

  addFooter(s, 15);
}

// ---------------- Write file ----------------
pres.writeFile({ fileName: OUT })
  .then(() => console.log("Wrote:", OUT))
  .catch((err) => console.error("Error:", err));
