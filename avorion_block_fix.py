import re
import sys
import shutil
from pathlib import Path

MIN_SIZE = 0.011
HALF_MIN = MIN_SIZE / 2.0
ROUND_DIGITS = 6

BLOCK_RE = re.compile(
    r'lx="(?P<lx>-?\d+\.?\d*)"\s+'
    r'ly="(?P<ly>-?\d+\.?\d*)"\s+'
    r'lz="(?P<lz>-?\d+\.?\d*)"\s+'
    r'ux="(?P<ux>-?\d+\.?\d*)"\s+'
    r'uy="(?P<uy>-?\d+\.?\d*)"\s+'
    r'uz="(?P<uz>-?\d+\.?\d*)"'
)


def fix_axis(l, u):
    original = u - l
    abs_original = abs(original)

    if abs_original >= MIN_SIZE:
        return l, u, abs_original, abs_original, False

    mid_pos = (l + u) / 2.0

    if original >= 0:
        new_l = mid_pos - HALF_MIN
        new_u = mid_pos + HALF_MIN
    else:
        new_l = mid_pos + HALF_MIN
        new_u = mid_pos - HALF_MIN

    new_l = round(new_l, ROUND_DIGITS)
    new_u = round(new_u, ROUND_DIGITS)

    new_abs = abs(new_u - new_l)

    return new_l, new_u, abs_original, new_abs, True


def process_file(input_path):
    input_path = Path(input_path).resolve()
    base_dir = input_path.parent

    backup_dir = base_dir / "Backup"
    backup_dir.mkdir(exist_ok=True)

    # Paths
    temp_fixed_path = base_dir / (input_path.stem + "__fixed.tmp")
    final_fixed_path = base_dir / input_path.name
    res_path = backup_dir / f"res_{input_path.name}.txt"

    script_path = Path(__file__).resolve()
    backup_script_path = backup_dir / script_path.name
    backup_original_path = backup_dir / input_path.name

    # --- Processing phase (NO overwriting) ---
    with input_path.open("r", encoding="utf-8") as fin, \
         temp_fixed_path.open("w", encoding="utf-8") as fout, \
         res_path.open("w", encoding="utf-8") as fres:

        for line_number, line in enumerate(fin, start=1):
            match = BLOCK_RE.search(line)

            if not match:
                fout.write(line)
                continue

            lx = float(match.group("lx"))
            ly = float(match.group("ly"))
            lz = float(match.group("lz"))
            ux = float(match.group("ux"))
            uy = float(match.group("uy"))
            uz = float(match.group("uz"))

            new_lx, new_ux, ox, nx, fx = fix_axis(lx, ux)
            new_ly, new_uy, oy, ny, fy = fix_axis(ly, uy)
            new_lz, new_uz, oz, nz, fz = fix_axis(lz, uz)

            if not (fx or fy or fz):
                fout.write(line)
                continue

            new_line = line
            new_line = new_line.replace(f'lx="{lx}"', f'lx="{new_lx:.6f}"')
            new_line = new_line.replace(f'ux="{ux}"', f'ux="{new_ux:.6f}"')
            new_line = new_line.replace(f'ly="{ly}"', f'ly="{new_ly:.6f}"')
            new_line = new_line.replace(f'uy="{uy}"', f'uy="{new_uy:.6f}"')
            new_line = new_line.replace(f'lz="{lz}"', f'lz="{new_lz:.6f}"')
            new_line = new_line.replace(f'uz="{uz}"', f'uz="{new_uz:.6f}"')

            fout.write(new_line)

            fres.write(f"line number: {line_number}\n")
            fres.write("original line:\n")
            fres.write(line)
            fres.write("altered line:\n")
            fres.write(new_line)
            fres.write(
                "dimensions:\n"
                f"ox: {ox:.6f}, oy: {oy:.6f}, oz: {oz:.6f} | "
                f"nx: {nx:.6f}, ny: {ny:.6f}, nz: {nz:.6f}\n\n\n"
            )

    # --- Safe file moves (order matters!) ---

    # 1) Move original ship to Backup
    shutil.move(str(input_path), str(backup_original_path))

    # 2) Move fixed temp file into original location/name
    shutil.move(str(temp_fixed_path), str(final_fixed_path))

    # 3) Move script itself to Backup
    if script_path.exists():
        shutil.move(str(script_path), str(backup_script_path))

    print("Processing complete.")
    print(f"Fixed ship ready: {final_fixed_path.name}")
    print(f"Backup folder: {backup_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python avorion_block_fix.py <shipfile.xml>")
        sys.exit(1)

    process_file(sys.argv[1])
