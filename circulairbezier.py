import math
def arc_to_beziers(cx, cy, r, start_deg, end_deg):
    """
    Convert a circular arc to cubic Bézier segments.
    Returns a list of segments: [(x1,y1, cx1,cy1, cx2,cy2, x2,y2), ...]
    """

    # Validate angles
    if not (isinstance(start_deg, (int, float)) and isinstance(end_deg, (int, float))):
        raise ValueError("start_deg and end_deg must be numeric")

    # Normalize angles to radians
    start = math.radians(start_deg)
    end = math.radians(end_deg)
    sweep = end - start

    if sweep == 0:
        return []

    # Split arc if larger than 90 degrees for accuracy
    max_sweep = math.radians(90)
    segments = max(1, int(abs(sweep) / max_sweep) + 1)
    delta = sweep / segments

    beziers = []
    angle1 = start

    for _ in range(segments):
        angle2 = angle1 + delta

        # Compute the endpoints
        x1 = cx + r * math.cos(angle1)
        y1 = cy + r * math.sin(angle1)
        x4 = cx + r * math.cos(angle2)
        y4 = cy + r * math.sin(angle2)

        # Cubic Bézier control point calculation for circular arcs
        t = math.tan(delta / 4) * 4 / 3

        cx1 = x1 - t * r * math.sin(angle1)
        cy1 = y1 + t * r * math.cos(angle1)
        cx2 = x4 + t * r * math.sin(angle2)
        cy2 = y4 - t * r * math.cos(angle2)

        beziers.append((x1, y1, cx1, cy1, cx2, cy2, x4, y4))

        angle1 = angle2

    return beziers


def make_svg(bezier_segments, width=300, height=300):
    """
    Build an SVG string from cubic Bézier segments.
    """

    if not bezier_segments:
        return "<svg></svg>"

    # Move-to the start point
    x0, y0 = bezier_segments[0][0], bezier_segments[0][1]
    path_data = f"M {x0:.4f},{y0:.4f}"

    # Add cubic Bézier segments
    for (x1, y1, cx1, cy1, cx2, cy2, x2, y2) in bezier_segments:
        path_data += f" C {cx1:.4f},{cy1:.4f} {cx2:.4f},{cy2:.4f} {x2:.4f},{y2:.4f}"

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">
  <path d="{path_data}" stroke="black" fill="none" stroke-width="2"/>
</svg>
"""
    return svg


# Example: 30-degree circular segment
try:
    beziers = arc_to_beziers(
        cx=150,      # center x
        cy=150,      # center y
        r=100,       # radius
        start_deg=0, # start angle
        end_deg=180   # end angle
    )

    svg_output = make_svg(beziers)

    # Save to file
    with open("SVG/arc_30deg.svg", "w") as f:
        f.write(svg_output)

    print(svg_output)

except Exception as e:
    print("Error:", e)
