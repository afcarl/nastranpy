from nastranpy.bdf.cards.enums import Seq
from nastranpy.bdf.cards.padding import Padding
from nastranpy.bdf.cards.field_info import FieldInfo as F


item_types = ('include', 'coord', 'elem', 'grid', 'mat', 'prop')
set_types = ('mpc', 'spc', 'load')
tag_types = ('e1D', 'e2D', 'e3D', 'eRigid', 'eSpring', 'eMass', 'ePlot')

item_type_sorting = {item_type: str(i).ljust(2, '0') for i, item_type in
                     enumerate(item_types + set_types)}

def sorted_cards(cards):
    return sorted(cards, key=lambda card: ('99' if card.type is None else
                                           item_type_sorting[card.type]) +
                                          card.name.ljust(8, '0') +
                                          str(card.id).rjust(8, '0'))

card_interfaces = {
    # Grids
    'GRID': ('GRID', 'grid',
             [F(), F(), F('CP', 'coord'), F('xyz', seq_type=Seq.vector), F('CD', 'coord', alternate_name='coord'), F('PS'), F('SEID')]),
    # Coordinate systems
    'CORD2R': ('CORD2R', 'coord',
               [F(), F(), F('RID', 'coord'), F('A', seq_type=Seq.vector), F('B', seq_type=Seq.vector),
                F('C', seq_type=Seq.vector)]),
    'CORD2C': ('CORD2C', 'coord',
               [F(), F(), F('RID', 'coord'), F('A', seq_type=Seq.vector), F('B', seq_type=Seq.vector),
                F('C', seq_type=Seq.vector)]),
    'CORD2S': ('CORD2S', 'coord',
               [F(), F(), F('RID', 'coord'), F('A', seq_type=Seq.vector), F('B', seq_type=Seq.vector),
                F('C', seq_type=Seq.vector)]),
    'CORD1R': ('CORD1R', 'coord',
               [F(), F(), F('G1A', 'grid'), F('G2A', 'grid'), F('G3A', 'grid'), F(other_card=True)]),
    'CORD1C': ('CORD1C', 'coord',
               [F(), F(), F('G1A', 'grid'), F('G2A', 'grid'), F('G3A', 'grid'), F(other_card=True)]),
    'CORD1S': ('CORD1S', 'coord',
               [F(), F(), F('G1A', 'grid'), F('G2A', 'grid'), F('G3A', 'grid'), F(other_card=True)]),
    # Materials
    'MAT1': ('MAT1', 'mat',
             [F(), F(), F('E'), F('G'), F('NU'), F('RHO'), F('A'), F('TREF'), F('GE'),
              F('ST'), F('SC'), F('SS'), F('MCSID', 'coord')]),
    'MAT2': ('MAT2', 'mat',
             [F(), F(), F('G11'), F('G12'), F('G13'), F('G22'), F('G23'), F('G33'), F('RHO'),
              F('A1'), F('A2'), F('A3'), F('TREF'), F('GE'), F('ST'), F('SC'), F('SS'),
              F('MCSID', 'coord')]),
    'MAT3': ('MAT3', 'mat',
             [F(), F(), F('EX'), F('ETH'), F('EZ'), F('NUXTH'), F('NUTHZ'), F('NUZX'), F('RHO'),
              F(), F(), F('GZX'), F('AX'), F('ATH'), F('AZ'), F('TREF'), F('GE')]),
    'MAT8': ('MAT8', 'mat',
             [F(), F(), F('E1'), F('E2'), F('NU12'), F('G12'), F('G1Z'), F('G2Z'), F('RHO'),
              F('A1'), F('A2'), F('TREF'), F('Xt'), F('Xc'), F('Yt'), F('Yc'), F('S'),
              F('GE'), F('F12'), F('STRN')]),
    'MAT9': ('MAT9', 'mat',
             [F(), F(), F('G11'), F('G12'), F('G13'), F('G14'), F('G15'), F('G16'), F('G22'),
              F('G23'), F('G24'), F('G25'), F('G26'), F('G33'), F('G34'), F('G35'), F('G36'),
              F('G44'), F('G45'), F('G46'), F('G55'), F('G56'), F('G66'), F('RHO'), F('A1'),
              F('A2'), F('A3'), F('A4'), F('A5'), F('A6'), F('TREF'), F('GE')]),
    # Elements
    'CROD': ('CROD', 'elem',
             [F(), F(), F('prop', 'prop'), F('grids', 'grid', seq_type=Seq.list, length=2, update_grid=True)], 'e1D'),
    'CONROD': ('CONROD', 'elem',
               [F(), F(), F('grids', 'grid', seq_type=Seq.list, length=2, update_grid=True), F('mat', 'mat'), F('A'), F('J'), F('C'), F('NSM')], 'e1D'),
    'CBAR': ('CBAR', 'elem',
             [F(), F(), F('prop', 'prop'), F('grids', 'grid', seq_type=Seq.list, length=2, update_grid=True), F('v', 'grid', seq_type=Seq.vector, alternate_name='G0'), F('OFFT'),
              F('PA'), F('PB'), F('offsetA', seq_type=Seq.vector), F('offsetB', seq_type=Seq.vector)], 'e1D'),
    'CBEAM': ('CBEAM', 'elem',
              [F(), F(), F('prop', 'prop'), F('grids', 'grid', seq_type=Seq.list, length=2, update_grid=True), F('v', 'grid', seq_type=Seq.vector, alternate_name='G0'), F('OFFT'),
               F('PA'), F('PB'), F('offsetA', seq_type=Seq.vector), F('offsetB', seq_type=Seq.vector),
               F('SA', 'grid'), F('SB', 'grid')], 'e1D'),
    'CQUAD4': ('CQUAD4', 'elem',
               [F(), F(), F('prop', 'prop'), F('grids', 'grid', seq_type=Seq.list, length=4, update_grid=True), F('THETA', 'coord', alternate_name='MCID'), F('ZOFFS'),
                F(), F('TFLAG'), F('T1'), F('T2'), F('T3'), F('T4')], 'e2D'),
    'CTRIA3': ('CTRIA3', 'elem',
               [F(), F(), F('prop', 'prop'), F('grids', 'grid', seq_type=Seq.list, length=3, update_grid=True), F('THETA', 'coord', alternate_name='MCID'), F('ZOFFS'),
                F(), F('TFLAG'), F('T1'), F('T2'), F('T3')], 'e2D'),
    'CTETRA': ('CTETRA', 'elem',
               [F(), F(), F('prop', 'prop'), F('grids', 'grid', seq_type=Seq.list, length=10, update_grid=True)], 'e3D'),
    'CPENTA': ('CPENTA', 'elem',
               [F(), F(), F('prop', 'prop'), F('grids', 'grid', seq_type=Seq.list, length=15, update_grid=True)], 'e3D'),
    'CHEXA': ('CHEXA', 'elem',
              [F(), F(), F('prop', 'prop'), F('grids', 'grid', seq_type=Seq.list, length=20, update_grid=True)], 'e3D'),
    'RBE2': ('RBE2', 'elem',
             [F(), F(), F('master_grid', 'grid', update_grid=True), F('CM'), F('slave_grids', 'grid', seq_type=Seq.set, update_grid=True), F('ALPHA')], 'eRigid'),
    'RBE3': ('RBE3', 'elem',
             [F(), F(), F(), F('master_grid', 'grid', update_grid=True), F('REFC'),
              F('slaves', seq_type=Seq.list, subscheme=[F('WT'), F('C'), F('grids', 'grid', seq_type=Seq.set, update_grid=True)]),
              F('UM', seq_type=Seq.list, subscheme=[F('GM', 'grid'), F('CM')], optional=True),
              F('ALPHA', optional=True)], 'eRigid'),
    'CBUSH': ('CBUSH', 'elem',
              [F(), F(), F('prop', 'prop'), F('grids', 'grid', seq_type=Seq.list, length=2, update_grid=True), F('v', 'grid', seq_type=Seq.vector, alternate_name='G0'), F('CID', 'coord'),
               F('S'), F('OCID', 'coord'), F('offset', seq_type=Seq.vector)], 'eSpring'),
    'CONM2': ('CONM2', 'elem',
              [F(), F(), F('grids', 'grid', seq_type=Seq.list, length=1, update_grid=True), F('CID', 'coord', alternate_name='coord'), F('M'), F('offset', seq_type=Seq.vector), F(),
               F('I11'), F('I21'), F('I22'), F('I31'), F('I32'), F('I33')], 'eMass'),
    'PLOTEL': ('PLOTEL', 'elem',
               [F(), F(), F('grids', 'grid', seq_type=Seq.list, length=2, update_grid=True)], 'ePlot'),
    # Properties
    'PROD': ('PROD', 'prop',
             [F(), F(), F('mat', 'mat'), F('A'), F('J'), F('C'), F('NSM')]),
    'PBAR': ('PBAR', 'prop',
             [F(), F(), F('mat', 'mat'), F('A'), F('I1'), F('I2'), F('J'), F('NSM'), F(),
              F('C1'), F('C2'), F('D1'), F('D2'), F('E1'), F('E2'), F('F1'), F('F2'),
              F('K1'), F('K2'), F('I12')]),
    'PBARL': ('PBARL', 'prop',
              [F(), F(), F('mat', 'mat'), F('GROUP'), F('TYPE'), F(), F(), F(), F(), F('data', seq_type=Seq.list, length=-1)]),
    'PBEAM': ('PBEAM', 'prop',
              [F(), F(), F('mat', 'mat'), F('A'), F('I1'), F('I2'), F('I12'), F('J'), F('NSM'),
               F('C1'), F('C2'), F('D1'), F('D2'), F('E1'), F('E2'), F('F1'), F('F2'),
               F('stations', seq_type=Seq.list, subscheme=[F('SO'), F('X_XB'), F('A'), F('I1'), F('I2'), F('I12'), F('J'), F('NSM'),
                                                           F('C1'), F('C2'), F('D1'), F('D2'), F('E1'), F('E2'), F('F1'), F('F2')]),
               F('K1'), F('K2'), F('S1'), F('S2'), F('NSI_A'), F('NSI_B'), F('CW_A'), F('CW_B'),
               F('M1_A'), F('M2_A'), F('M1_B'), F('M2_B'), F('N1_A'), F('N2_A'), F('N1_B'), F('N2_B')]),
    'PBEAML': ('PBEAML', 'prop',
               [F(), F(), F('mat', 'mat'), F('GROUP'), F('TYPE'), F(), F(), F(), F(), F('data', seq_type=Seq.list, length=-1)]),
    'PSHELL': ('PSHELL', 'prop',
               [F(), F(), F('mat1', 'mat'), F('T', alternate_name='thickness'), F('mat2', 'mat'), F('BMIR'), F('mat3', 'mat'), F('TST'), F('NSM'),
                F('Z1'), F('Z2'), F('mat4', 'mat')]),
    'PCOMP': ('PCOMP', 'prop',
              [F(), F(), F('Z0'), F('NSM'), F('SB'), F('FT'), F('TREF'), F('GE'), F('LAM'),
               F('plies', seq_type=Seq.list, subscheme=[F('mat', 'mat'), F('T'), F('THETA'), F('SOUT')])]),
    'PCOMPG': ('PCOMPG', 'prop',
               [F(), F(), F('Z0'), F('NSM'), F('SB'), F('FT'), F('TREF'), F('GE'), F('LAM'),
                F('plies', seq_type=Seq.list, subscheme=[F('id'), F('mat', 'mat'), F('T'), F('THETA'), F('SOUT')])], None, Padding(9, {6, 7, 8})),
    'PSOLID': ('PSOLID', 'prop',
               [F(), F(), F('mat', 'mat'), F('CORDM', 'coord'), F('IN'), F('STRESS'), F('ISOP'), F('FCTN'), F('COROT')]),
    'PBUSH': ('PBUSH', 'prop',
              [F(), F(),
               F('K', subscheme=[F('K1'), F('K2'), F('K3'), F('K4'), F('K5'), F('K6')], optional=True),
               F('B', subscheme=[F('B1'), F('B2'), F('B3'), F('B4'), F('B5'), F('B6')], optional=True),
               F('GE', subscheme=[F('GE1'), F('GE2'), F('GE3'), F('GE4'), F('GE5'), F('GE6')], optional=True),
               F('RCV', subscheme=[F('SA'), F('ST'), F('EA'), F('ET')], optional=True),
               F('M', optional=True)], None, Padding(9, {1})),
    # MPCs
    'MPC': ('MPC', 'mpc',
            [F(), F(), F('equation', seq_type=Seq.list, subscheme=[F('G', 'grid'), F('C'), F('A')])], None, Padding(8, {1, 8})),
    'MPCADD': ('MPCADD', 'mpc',
               [F(), F(), F('sets', 'mpc', seq_type=Seq.set)]),
    # SPCs
    'SPC': ('SPC', 'spc',
            [F(), F(), F('G1', 'grid'), F('C1'), F('D1'), F('G2', 'grid'), F('C2'), F('D2')]),
    'SPCD': ('SPCD', 'spc',
             [F(), F(), F('G1', 'grid'), F('C1'), F('D1'), F('G2', 'grid'), F('C2'), F('D2')]),
    'SPC1': ('SPC1', 'spc',
             [F(), F(), F('C'), F('grids', 'grid', seq_type=Seq.set)]),
    'SPCADD': ('SPCADD', 'spc',
               [F(), F(), F('sets', 'spc', seq_type=Seq.set)]),
    # LOADs
    'FORCE': ('FORCE', 'load',
              [F(), F(), F('G', 'grid'), F('CID', 'coord'), F('F'), F('n', seq_type=Seq.vector)]),
    'MOMENT': ('MOMENT', 'load',
               [F(), F(), F('G', 'grid'), F('CID', 'coord'), F('M'), F('n', seq_type=Seq.vector)]),
    'PLOAD4': ('PLOAD4', 'load',
               [F(), F(), F('elem', 'elem'), F('P1'), F('P2'), F('P3'), F('P4'), F('G1', 'grid'), F('G3', 'grid', alternate_name='G4'),
                F('CID', 'coord'), F('n', seq_type=Seq.vector), F('SORL'), F('LDIR')]),
    # Other
    'INCLUDE': ('INCLUDE', 'include'),
}
