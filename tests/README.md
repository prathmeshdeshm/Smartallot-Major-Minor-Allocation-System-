# Unit Tests for SmartAllot

This directory contains unit tests for the allocation and eligibility logic.

## Running Tests

⚠️ **Note**: Due to the non-standard Django project structure (app files in root directory instead of a proper app package), tests cannot be run using the standard `python manage.py test` command without restructuring.

### Option 1: Restructure the Project (Recommended for Production)

To properly run these tests, the project should be restructured into a standard Django layout:

```
smartallot/                    # Project root
├── manage.py
├── smartallot/               # Project config package
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── allotment/                # App package  
    ├── __init__.py
    ├── models.py
    ├── views.py
    ├── utils.py
    ├── forms.py
    ├── admin.py
    └── tests/
        ├── __init__.py
        └── test_utils.py
```

After restructuring, run tests with:
```bash
python manage.py test allotment.tests
```

### Option 2: Quick Verification

The tests are syntactically correct and test the following:

**Eligibility Tests (`EligibilityTestCase`)**:
- `test_student_eligible_no_rules`: Students eligible when no rules
- `test_student_eligible_min_percentage`: Minimum percentage requirement
- `test_student_eligible_department_block`: Department blocking
- `test_student_eligible_inactive_rule`: Inactive rules don't apply
- `test_oe_eligibility_*`: Same tests for Open Electives

**Allocation Tests (`AllocationTestCase`)**:
- `test_allocation_by_merit`: Higher merit student gets seat when capacity is limited
- `test_allocation_with_eligibility_rule`: Ineligible students don't get allocated
- `test_allocation_clears_previous`: Re-running allocation clears old data
- `test_no_allocation_when_capacity_full`: Zero capacity prevents allocation

## Test Coverage

These tests cover the core business logic in `utils.py`:
- `is_student_eligible(student, branch)` - Minor eligibility checking
- `is_student_eligible_for_oe(student, oe_subject)` - OE eligibility checking  
- `run_minor1_allocation()` - First minor allocation algorithm

## Future Improvements

- Add tests for `run_minor2_allocation()`
- Add tests for `run_oe_allocation()`
- Add integration tests for the full allocation workflow
- Add tests for edge cases (tie-breaking, simultaneous submissions, etc.)
