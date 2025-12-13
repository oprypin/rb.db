import pytest

from build.gen_part_details import find_overlay_from_part_name


@pytest.mark.parametrize('inp,outp', [
    ['Axle Hose, Soft 7L', '7'],  # 32580
    ['Bar 3L', '3'],  # 87994
    ['Bar 3L', '3'],  # 87994
    ['Bar 6L with Stop Ring', '6'],  # 63965
    ['Bar 6L with Stop Ring', '6'],  # 63965
    ['Baseplate 32 x 32', '32'],  # 3811
    ['Brick 1 x 16', '16'],  # 2465
    ['Brick 1 x 6', '6'],  # 3009
    ['Brick 2 x 8', '8'],  # 3007
    ['Brick Curved 10 x 1 [Symmetric Inside Ridges]', '10'],  # 13731
    ['Brick Round Corner, Curved 2 x 2 x 2/3 Quarter Circle', '2'],  # 5852
    ['Brick Round Corner, Curved 3 x 3 x 1 Quarter Circle', '3'],  # 76797
    ['Dish 2 x 2 Inverted [Radar]', '2'],  # 4740
    ['Dish 6 x 6 Inverted (Radar) with Solid Studs', '6'],  # 44375b
    ['Hose Rigid 3mm D. 24L / 19.2cm', '24'],  # 75c24
    ['Plate 1 x 4', '4'],  # 3710
    ['Plate 1 x 5', '5'],  # 78329
    ['Plate 2 x 6', '6'],  # 3795
    ['Plate 2 x 8', '8'],  # 3034
    ['Plate 8 x 16', '16'],  # 92438
    ['Plate 8 x 8', '8'],  # 41539
    ['Technic Axle 2 Notched', '2'],  # 32062
    ['Technic Axle 5.5 with Stop [Rounded Short End]', '5.5'],  # 59426
    ['Technic Axle 9', '9'],  # 60485
    ['Technic Axle and Pin Connector Angled #6 - 90°', '#6'],  # 32014
    ['Technic Beam 1 x 11 Thick with Alternating Holes', '11'],  # 73507
    ['Technic Beam 1 x 5 Thick', '5'],  # 32316
    ['Technic Beam 1 x 9 Thick with Alternating Holes', '9'],  # 6612
    ['Technic Brick 1 x 8 [7 Pin Holes]', '8'],  # 3702
    ['Technic Link 1 x 8', '8'],  # 5996
    ['Technic Panel Fairing # 4 Small Smooth Long, Side B', '#4'],  # 64391
    ['Technic Panel Fairing #21 5L Small Smooth, Side B', '#21'],  # 11946
    ['Technic Plate 2 x 8 [7 Holes]', '8'],  # 3738
    ['Tile 1 x 1 with Groove', '1'],  # 3070b
    ['Tile 1 x 2 with Groove', '2'],  # 3069b
    ['Tile 1 x 3', '3'],  # 63864
    ['Tile 1 x 8 with Groove', '8'],  # 4162
    ['Tile 2 x 2 with Groove', '2'],  # 3068b
    ['Tile 2 x 3', '3'],  # 26603
    ['Tile 2 x 4 with Groove', '4'],  # 87079
    ['Tile 6 x 6 with Bottom Tubes', '6'],  # 10202
    ['Tile Round 3 x 3', '3'],  # 67095
])
def test_returns_overlay_like_rebrickable(inp, outp):
    assert find_overlay_from_part_name(inp) == outp


@pytest.mark.parametrize('inp,outp', [
    ['Baseplate 16 x 32', '32'],  # 3857
    ['Brick Curved 1 x 4 x 2/3 Double, No Studs', '4'],  # 79756
    ['Brick Curved 2 x 4 x 1', '4'],  # 5842
    ['Brick Round Corner 4 x 4 x 1 with Bottom Cut Outs, No Studs, Flat Top', '4'],  # 5649
    ['Brick Round Corner 5 x 5 x 1 Curved, Bottom Cut Outs, No Studs, 9 Bottom Tubes', '5'],  # 7033
    ['Hose, Pneumatic 4mm D. 50L / 400mm', '50'],  # 5102c50
    ['Panel 1 x 3 x 1', '3'],  # 23950
    ['Panel 1 x 4 x 1 with Rounded Corners [Thin Wall]', '4'],  # 15207
    ['Plate Round 6 x 6 with Hole', '6'],  # 11213
    ['Plate Round Corner 6 x 6', '6'],  # 6003
    ['Plate Special 1 x 4 Rounded with 2 Open Studs', '4'],  # 77845
    ['Plate Special 1 x 8 with Door Rail', '8'],  # 4510
    ['Slope 18° 4 x 1', '4'],  # 60477
    ['Slope 18° 4 x 2', '4'],  # 30363
    ['Slope Curved 1 x 4 with Stud Notch Right', '4'],  # 5414
    ['Slope Curved 3 x 2 No Studs', '3'],  # 24309
    ['Slope Curved 3 x 2 with Stud Notch Left', '3'],  # 80177
    ['Slope Curved 4 x 2 No Studs', '4'],  # 93606
    ['Wedge Curved 10 x 3 Right', '10'],  # 50956
    ['Wedge Curved 8 x 3 x 2 Open Right', '8'],  # 41749
    ['Wedge Plate 12 x 3 Left', '12'],  # 47397
    ['Wedge Plate 6 x 2 Right', '6'],  # 78444
])
def test_returns_overlay_unlike_rebrickable(inp, outp):
    assert find_overlay_from_part_name(inp) == outp


@pytest.mark.parametrize('inp', [
    'Antenna 1 x 4 with Flat Top',  # 3957b
    'Bar 2L with Stop in Center',  # 78258
    'Brick 1 x 4',  # 3010
    'Brick 2 x 4',  # 3001
    'Brick Special 2 x 4 with 3 Axle Holes',  # 39789
    'Fence Lattice 1 x 4 x 1',  # 3633
    'Modulex Tile 1 x 3 with Internal Support',  # 1031B
    'Panel 1 x 2 x 1 [Rounded Corners]',  # 4865b
    'Plate 1 x 4 with 2 Bottom Pins',  # 68382
    'Plate 2 x 4',  # 3020
    'Plate 4 x 4',  # 3031
    'Plate Round 1 x 1 with Hollow Stud and Horizontal Bar 1L',  # 32828
    'Plate Round Corner 4 x 4',  # 30565
    'Plate Special 1 x 2 with 1 Stud with Groove and Inside Stud Holder (Jumper)',  # 15573
    'Plate Special 1 x 2 with Door Rail',  # 32028
    'Plate Special 1 x 4 Offset with Bar Holes',  # 4590
    'Plate Special 1 x 4 with 2 Studs with Groove [New Underside]',  # 41740
    'Plate Special 1 x 4 with Angled Tubes',  # 61072
    'Plate Special 4 x 6 with Trap Door Hinge [Long Pins]',  # 92099
    'Plate Special 6 x 8 Trap Door Frame Horizontal [Long Pin Holders]',  # 92107
    'Plate Special Round 2 x 2 with Center Stud (Jumper Plate)',  # 18674
    'Slope Curved 2 x 1 No Studs [1/2 Bow]',  # 11477
    'Slope Curved 3 x 4 x 2/3 Triple Curved with 2 Sunk Studs',  # 93604
    'Slope Curved 4 x 1 Double with No Studs',  # 93273
    'Slope Curved 4 x 1 Inverted',  # 13547
    'Slope Inverted 33° 3 x 1 with Internal Stopper and No Front Stud Connection',  # 4287c
    'Technic Axle 1.5 with Perpendicular Axle Connector (Technic Pole Reverser Handle)',  # 6553
    'Technic Axle Pin 3L with Friction Ridges Lengthwise and 1L Axle',  # 11214
    'Technic Beam 1 x 4 Thin',  # 32449
    'Technic Beam 1 x 9 Bent (7 - 3) Thick',  # 32271
    'Technic Beam 2 x 5 L-Shape with Quarter Ellipse Thick',  # 80286
    'Technic Brick 1 x 4 [3 Pin Holes]',  # 3701
    'Technic Brick 4 x 6 with 2 x 4 Opening',  # 32531
    'Technic Pin Connector Round 1L [Beam]',  # 18654
    'Technic Plate 1 x 5 with Smooth Ends, 4 Studs and Centre Axle Hole',  # 32124
    'Tile 2 x 2 Curved, Macaroni',  # 27925
    'Tile Round 2 x 2 with Bottom Stud Holder',  # 14769
    'Tile Round 2 x 4',  # 66857
    'Train Wheel RC Train, Metal Axle 5 x 100 LDU',  # 57051
    'Wedge Plate 4 x 6',  # 47407
])
def test_no_overlay_like_rebrickable(inp):
    assert find_overlay_from_part_name(inp) is None
