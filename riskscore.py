"""CARPREG II implementation of risk scores

#TODO: extend for other scores, build general framework"""

from more_itertools import always_iterable

predictors = {
    "Prior cardiac events or arrhythmias": 3,
    "Baseline NYHA III-IV or cyanosis": 3,
    "Mechanical valve": 3,
    "Ventricular dysfunction": 2,
    "High risk left-sided valve disease/left ventricular outflow tract obstruction": 2,
    "Pulmonary hypertension": 2,
    "Coronary artery disease": 2,
    "High risk aortopath": 2,
    "No prior cardiac intervention": 1,
    "Late pregnancy assessment": 1,
}

risk_pct = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15, 4: 0.22, 5: 0.41}


class UnknownRiskFactor(Exception):
    """"""


def calculate_risk_score(factors: str | list[str]) -> int:
    try:
        score = sum(predictors[factor] for factor in always_iterable(factors))
    except KeyError as e:
        raise UnknownRiskFactor(
            f"The provided risk factor {e} is not registered"
        ) from e
    return score


def calculate_risk_percentage(score: int) -> float:
    bounded_score = min(max(min(risk_pct), score), max(risk_pct))
    return risk_pct[bounded_score]
