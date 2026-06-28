"""
Tests for planes.py — focused on the thing that matters: the verification layer
actually CATCHES disagreements now, instead of comparing values to themselves.

Run:  python3 -m pytest tests/ -q
 or:  python3 tests/test_planes.py   (falls back to a tiny runner, no pytest needed)
"""

from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from planes import (  # noqa: E402
    inch, Assembly, FasciaDetail, DoorJamb, Threshold,
    Severity, run_validation, assert_coplanar,
    nearest_stock, plies_required, STD_STOCK_MM, MAX_STOCK_MM,
)


def make_wall() -> Assembly:
    return (Assembly("test wall", "ext face sheathing")
            .add("ext insulation", inch(1.5))
            .add("rainscreen gap", inch(0.75), is_drainage_gap=True)
            .add("cross furring", inch(0.75))
            .add("cladding", inch(0.75)))


def has_clash(issues) -> bool:
    return any(i.severity is Severity.CLASH for i in issues)


# --- stack arithmetic -------------------------------------------------------
def test_finish_and_cladding_planes():
    w = make_wall()
    assert abs(w.finish_plane - inch(3.75)) < 1e-6
    # cladding is the outermost solid; here it equals finish_plane
    assert abs(w.cladding_plane - inch(3.75)) < 1e-6


def test_cladding_plane_skips_trailing_gap():
    w = (Assembly("w", "d")
         .add("cladding", inch(0.75))
         .add("trailing gap", inch(0.75), is_drainage_gap=True))
    assert abs(w.finish_plane - inch(1.5)) < 1e-6
    assert abs(w.cladding_plane - inch(0.75)) < 1e-6  # gap excluded


def test_offset_after_unknown_raises():
    w = make_wall()
    try:
        w.offset_after("nope")
    except KeyError:
        return
    raise AssertionError("expected KeyError")


# --- clean build passes -----------------------------------------------------
def test_clean_build_no_clash():
    w = make_wall()
    issues = run_validation(
        FasciaDetail(wall=w, base_fascia_face=inch(0.5)),
        DoorJamb(wall=w, frame_face=0.0, casing="proud", proud_reveal=inch(0.125)),
        Threshold(wall=w, frame_sill_face=0.0, interior_floor_top=0.0,
                  step_down=inch(0.5)),
    )
    assert not has_clash(issues)


# --- the real guards: external `expect=` mismatches must CLASH ---------------
def test_jamb_expect_mismatch_clashes():
    w = make_wall()
    # derived extension is 95.25; feed a stale external number from "another drawing"
    issues = DoorJamb(wall=w, frame_face=0.0, expect_extension=80.0).validate()
    assert has_clash(issues)


def test_jamb_expect_match_ok():
    w = make_wall()
    issues = DoorJamb(wall=w, frame_face=0.0,
                      expect_extension=w.finish_plane).validate()
    assert not has_clash(issues)


def test_threshold_expect_mismatch_clashes():
    w = make_wall()
    issues = Threshold(wall=w, frame_sill_face=0.0, interior_floor_top=0.0,
                       expect_extension=50.0).validate()
    assert has_clash(issues)


def test_fascia_expect_mismatch_clashes():
    w = make_wall()
    issues = FasciaDetail(wall=w, base_fascia_face=inch(0.5),
                          expect_face=10.0).validate()
    assert has_clash(issues)


# --- geometry clashes -------------------------------------------------------
def test_frame_proud_of_finish_clashes():
    w = make_wall()
    # frame set 10 mm beyond the finish plane -> impossible jamb extension
    issues = DoorJamb(wall=w, frame_face=w.finish_plane + 10.0).validate()
    assert has_clash(issues)


def test_fascia_inside_cladding_clashes():
    w = make_wall()
    # base fascia already proud of the cladding plane -> can't build inward
    issues = FasciaDetail(wall=w, base_fascia_face=w.cladding_plane + 10.0).validate()
    assert has_clash(issues)


def test_sill_outside_cladding_clashes():
    w = make_wall()
    issues = Threshold(wall=w, frame_sill_face=w.cladding_plane + 10.0,
                       interior_floor_top=0.0).validate()
    assert has_clash(issues)


# --- threshold pan slope (slope-based, not absolute-fall) --------------------
def test_pan_slope_below_min_warns():
    w = make_wall()
    issues = Threshold(wall=w, frame_sill_face=0.0, interior_floor_top=0.0,
                       pan_slope_pct=1.0, min_slope_pct=2.0).validate()
    assert any(i.where == "threshold-pan" and i.severity is Severity.WARN
               for i in issues)


def test_pan_slope_adequate_ok_on_short_reach():
    w = make_wall()  # short ~95 mm reach must NOT warn when slope is adequate
    issues = Threshold(wall=w, frame_sill_face=0.0, interior_floor_top=0.0,
                       pan_slope_pct=2.0, min_slope_pct=2.0).validate()
    assert all(i.severity is not Severity.WARN
               for i in issues if i.where == "threshold-pan")


# --- assert_coplanar genuinely fails ----------------------------------------
def test_assert_coplanar_detects_spread():
    issues = assert_coplanar("front", tol=1.0, a=95.0, b=95.5, c=120.0)
    assert has_clash(issues)


def test_assert_coplanar_within_tol_ok():
    issues = assert_coplanar("front", tol=1.0, a=95.0, b=95.4)
    assert not has_clash(issues)


# --- jamb edge cases (the fixes) --------------------------------------------
def test_jamb_zero_extension_no_stock_warn():
    w = make_wall()
    # frame flush with the finish plane -> no extension; must NOT warn about stock
    issues = DoorJamb(wall=w, frame_face=w.finish_plane).validate()
    assert not has_clash(issues)
    assert not any(i.severity is Severity.WARN for i in issues)
    assert any("no jamb extension required" in i.msg for i in issues)


def test_head_flashing_insufficient_drip_warns():
    w = make_wall()
    # positive but tiny drip -> not a clash, but below min -> WARN
    issues = DoorJamb(wall=w, frame_face=0.0, head_drip=1.0).validate()
    assert not has_clash(issues)
    assert any(i.where == "jamb-head" and i.severity is Severity.WARN
               for i in issues)


def test_head_flashing_zero_drip_clashes():
    w = make_wall()
    issues = DoorJamb(wall=w, frame_face=0.0, head_drip=0.0).validate()
    assert has_clash(issues)


def test_head_flashing_adequate_drip_ok():
    w = make_wall()
    issues = DoorJamb(wall=w, frame_face=0.0, head_drip=inch(0.5)).validate()
    assert not any(i.where == "jamb-head" and i.severity is not Severity.OK
                   for i in issues)


# --- stock / ply math -------------------------------------------------------
def test_std_stock_keeps_real_lumber():
    # the dressed 1.5" 2x (38.1 mm) must be present, not a 38.0 rounded twin
    assert any(abs(s - inch(1.5)) < 0.05 for s in STD_STOCK_MM)
    assert abs(MAX_STOCK_MM - inch(1.5)) < 0.05

def test_plies_required_no_off_by_one():
    # exactly 2 plies of the thickest stock should report 2, not 3
    assert plies_required(2 * MAX_STOCK_MM) == 2
    assert plies_required(2 * MAX_STOCK_MM + 0.1) == 3
    assert plies_required(0.0) == 1  # never zero


def test_std_stock_deduped_sorted():
    assert list(STD_STOCK_MM) == sorted(STD_STOCK_MM)
    # no two entries within 0.5 mm of each other after de-dup
    for a, b in zip(STD_STOCK_MM, STD_STOCK_MM[1:]):
        assert b - a > 0.5


def test_nearest_stock_exact_and_over():
    stock, leftover = nearest_stock(MAX_STOCK_MM)  # exact single piece
    assert stock is not None and abs(leftover) < 0.6
    stock, _ = nearest_stock(MAX_STOCK_MM + 50)    # beyond any single piece
    assert stock is None


# --- tiny runner so this works without pytest -------------------------------
def _run_all():
    fns = [v for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    passed = 0
    for fn in fns:
        fn()
        passed += 1
        print(f"  ok  {fn.__name__}")
    print(f"\n{passed}/{len(fns)} tests passed")


if __name__ == "__main__":
    _run_all()
