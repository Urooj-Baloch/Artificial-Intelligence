from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.models import DiscreteBayesianNetwork

model = DiscreteBayesianNetwork([
    ('Intelligence', 'Grade'),
    ('StudyHours', 'Grade'),
    ('Difficulty', 'Grade'),
    ('Grade', 'Pass')
])

cpd_I = TabularCPD('Intelligence', 2, [[0.7], [0.3]], state_names={'Intelligence': ['High', 'Low']})
cpd_S = TabularCPD('StudyHours', 2, [[0.6], [0.4]], state_names={'StudyHours': ['Sufficient', 'Insufficient']})
cpd_D = TabularCPD('Difficulty', 2, [[0.6], [0.4]], state_names={'Difficulty': ['Easy', 'Hard']})

cpd_G = TabularCPD(
    'Grade', 3,
    values=[
        [0.8, 0.6, 0.6, 0.4, 0.5, 0.3, 0.2, 0.1],
        [0.15, 0.3, 0.3, 0.4, 0.35, 0.4, 0.4, 0.3],
        [0.05, 0.1, 0.1, 0.2, 0.15, 0.3, 0.4, 0.6],
    ],
    evidence=['Intelligence', 'StudyHours', 'Difficulty'],
    evidence_card=[2, 2, 2],
    state_names={
        'Grade': ['A', 'B', 'C'],
        'Intelligence': ['High', 'Low'],
        'StudyHours': ['Sufficient', 'Insufficient'],
        'Difficulty': ['Easy', 'Hard']
    }
)

cpd_P = TabularCPD(
    'Pass', 2,
    values=[
        [0.05, 0.2, 0.5],
        [0.95, 0.8, 0.5]
    ],
    evidence=['Grade'],
    evidence_card=[3],
    state_names={
        'Pass': ['No', 'Yes'],
        'Grade': ['A', 'B', 'C']
    }
)

model.add_cpds(cpd_I, cpd_S, cpd_D, cpd_G, cpd_P)
model.check_model()

infer = VariableElimination(model)

q1 = infer.query(variables=['Pass'], evidence={'StudyHours': 'Sufficient', 'Difficulty': 'Hard'})
print(q1)

q2 = infer.query(variables=['Intelligence'], evidence={'Pass': 'Yes'})
print(q2)