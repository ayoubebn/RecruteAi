def filter_candidates(cv_skills, job_skills):
    return set(cv_skills).issubset(set(job_skills))
