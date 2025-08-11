from app import models

def create_policies(db_session, count=1, **kwargs):
    """Factory for creating test Policy entries."""
    policies = []
    for i in range(count):
        policy = models.Policy(
            name=f"Policy {i+1}",
            days_allowed=10,
            policy_type="Annual",
            **kwargs
        )
        db_session.add(policy)
        policies.append(policy)
    db_session.commit()
    return policies