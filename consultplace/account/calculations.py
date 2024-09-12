def calculate_rating(
    personal_grade, deadline_compliance,
    manager_recommendation, group_grade, intricacy_coefficient
):
    if (
        personal_grade is not None
        and deadline_compliance is not None
        and manager_recommendation is not None
        and group_grade is not None
        and intricacy_coefficient is not None
    ):
        rating = round(
            (
                0.3 * personal_grade
                + 0.2 * deadline_compliance
                + 0.2 * manager_recommendation
                + 0.3 * group_grade
            ) * intricacy_coefficient, 1
        )
        return rating
