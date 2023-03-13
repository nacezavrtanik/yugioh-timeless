
def supervised_input(prompt, conditions):
    """Require user input to satisfy specified conditions.

    The user is asked to provide an input value. If the provided value violates
    a specified condition, a tip for correcting the input is displayed, then
    the user is once again asked to provide an input value. This process is
    repeated until all specified conditions are satisfied.

    Parameters
    ----------
    prompt : str
        Description of desired input.
    conditions: str, list of str
        Names of conditions. A string can be passed if only one condition is
        specified, otherwise a list of strings.

    Returns
    -------
    str
        User input, satisfying all conditions in `conditions`.
    """

    condition_checks = {
        '1_or_2': lambda input_string: input_string in ['1', '2'],
        '1_2_or_3': lambda input_string: input_string in ['1', '2', '3']
    }

    input_tips = {
        '1_or_2': 'Enter either 1 or 2.',
        '1_2_or_3': 'Enter either 1, 2, or 3.'
    }

    if isinstance(conditions, str):
        conditions = [conditions]

    while True:

        user_input = input(prompt)
        check = True

        for condition in conditions:

            condition_satisfied = condition_checks.get(condition)(user_input)
            check = check and condition_satisfied

            if not condition_satisfied:
                print(f'TIP: {input_tips.get(condition)}')
                break

        if check:
            return user_input
