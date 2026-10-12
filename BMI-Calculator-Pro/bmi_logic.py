def calculate_bmi(weight, height_cm):
    """
    Calculate BMI using:
        BMI = weight(kg) / height(m)^2

    Returns:
        bmi, category, color, advice
    """

    if weight <= 0:
        raise ValueError("Weight must be greater than 0.")

    if height_cm <= 0:
        raise ValueError("Height must be greater than 0.")

    height_m = height_cm / 100

    bmi = round(weight / (height_m ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
        color = "#FFA500"
        advice = (
            "Your BMI is below the healthy range. "
            "Maintain a balanced diet and consider professional guidance."
        )

    elif bmi < 25:
        category = "Normal"
        color = "#00E676"
        advice = (
            "Excellent! Your BMI is within the healthy range. "
            "Maintain your current healthy lifestyle."
        )

    elif bmi < 30:
        category = "Overweight"
        color = "#FF7043"
        advice = (
            "Your BMI is above the healthy range. "
            "Regular physical activity and a balanced diet may help."
        )

    else:
        category = "Obese"
        color = "#FF3D3D"
        advice = (
            "Your BMI is in the obese range. "
            "Consider consulting a qualified healthcare professional."
        )

    return bmi, category, color, advice