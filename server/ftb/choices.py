GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

VISUAL_LOSS_AGE_CHOICES = (
    (00, 'Since Birth'),
    (88, 'First Year of life'),
    (99, 'Unknown')
) + tuple(zip(range(1, 15), ("{0} in Years".format(years) for years in range(1, 15))))
