# Minimal Cover

This project aims to find the minimal cover for a given functional dependency set and relation R.

Problem Description
Given a functional dependency set of `{("A", "BE"), ("A", "C"), ("C", "B"), ("D", "F"), ("C", "R")}` and a relation R of `("A", "B", "C", "D", "E")`, the task is to find the minimal cover for the functional dependency set.

## Solution

To find the minimal cover, the following steps are taken:

1. **Simplify the functional dependency set:** Each functional dependency is simplified such that there is only one attribute on the right-hand side.

   **Result:** `{A->B, A->E, A->C, C->B, D->F, C->R}`

2. **Remove the functional dependencies that don't belong to the relation R:** Any functional dependencies that contain attributes not belonging to the relation are removed. In this case, `D->F` and `C->R` are removed as they contain attributes `F` and `R` respectively which do not belong to the relation R.

   **Result:** `{A->B, A->E, A->C, C->B}`

3. **Remove extraneous attributes:** Any extraneous attributes from the left-hand side of the functional dependencies are removed.

4. **Remove redundant functional dependencies:** Any redundant functional dependencies from the set are eliminated by finding the closure of the left-hand side of each functional dependency and checking if the right-hand side can be inferred from it. Any functional dependencies where this is the case are considered redundant and removed.

   **Result:** `{A->E, A->C, C->B}`

## Final Result

The minimal cover of the functional dependency set is `{A->E, A->C, C->B}`.

**Note:** The 3rd point is not included in the code yet, but it's an important step in finding the minimal cover.

## Run the code

    python fd_minimal_cover.py

## Future

1. At present, only alphabetic characters are allowed in the construction of FD sets.
2. Include the third point 'remove extraneous features'.
3. Works correctly when only one character is present in the LHS.
