"""
services/decision_service.py

Adaptive decision engine for TwinLearnAI.

The DecisionService analyzes student performance
and selects an appropriate teaching strategy.
"""

from sqlalchemy.orm import Session

from models.test_result import TestResult


class DecisionService:
    """
    Responsible for selecting the teaching strategy
    based on student performance.
    """

    # ========================================================
    # DEFAULT STRATEGY
    # ========================================================

    DEFAULT_STRATEGY = "story based"

    # ========================================================
    # THRESHOLDS
    # ========================================================

    VERY_LOW_SCORE_THRESHOLD = 50.0

    RECENT_TEST_THRESHOLD = 80.0

    DIAGRAM_ACCURACY_THRESHOLD = 50.0

    RECENT_TEST_COUNT = 3

    # ========================================================
    # MAIN DECISION FUNCTION
    # ========================================================

    @staticmethod
    def select_strategy(
        db: Session,
        student_db_id: int,
    ) -> dict:
        """
        Select the appropriate teaching strategy
        based on student performance.

        Decision priority:

        Rule 1:
            Latest score < 50%
            -> story based

        Rule 2:
            Last 3 tests are all below 80%
            -> diagram based

        Rule 3:
            Diagram accuracy < 50%
            -> diagram based

        Rule 4:
            Otherwise
            -> story based
        """

        # ====================================================
        # FETCH RECENT TEST RESULTS
        # ====================================================

        recent_tests = (
            db.query(TestResult)
            .filter(
                TestResult.student_id == student_db_id
            )
            .order_by(
                TestResult.created_at.desc()
            )
            .limit(
                DecisionService.RECENT_TEST_COUNT
            )
            .all()
        )

        # ====================================================
        # NO TEST DATA
        # ====================================================

        if not recent_tests:

            return {
                "strategy": DecisionService.DEFAULT_STRATEGY,
                "reason": (
                    "No test performance data is available. "
                    "Using the default story-based teaching strategy."
                ),
                "score": None,
                "rule": "default",
            }

        # ====================================================
        # LATEST TEST
        # ====================================================

        latest_test = recent_tests[0]

        latest_score = latest_test.percentage

        # ====================================================
        # RULE 1
        # LATEST SCORE < 50%
        # ====================================================

        if latest_score < DecisionService.VERY_LOW_SCORE_THRESHOLD:

            return {
                "strategy": "story based",
                "reason": (
                    f"The student's latest test score is "
                    f"{latest_score:.1f}%, which is below 50%. "
                    "A story-based strategy is selected to "
                    "simplify the concept."
                ),
                "score": latest_score,
                "rule": "latest_score_below_50",
            }

        # ====================================================
        # RULE 2
        # LAST 3 TESTS ALL < 80%
        # ====================================================

        if len(recent_tests) >= DecisionService.RECENT_TEST_COUNT:

            last_three_below_80 = all(
                test.percentage
                < DecisionService.RECENT_TEST_THRESHOLD
                for test in recent_tests
            )

            if last_three_below_80:

                scores = [
                    round(test.percentage, 1)
                    for test in recent_tests
                ]

                return {
                    "strategy": "diagram based",
                    "reason": (
                        "The student's last 3 test scores "
                        f"are {scores}, all below 80%. "
                        "A diagram-based strategy is selected "
                        "to provide more visual explanations."
                    ),
                    "score": latest_score,
                    "rule": "last_3_tests_below_80",
                }

        # ====================================================
        # RULE 3
        # DIAGRAM ACCURACY < 50%
        # ====================================================

        if latest_test.diagram_questions > 0:

            diagram_accuracy = (
                latest_test.diagram_correct
                / latest_test.diagram_questions
            ) * 100

            if (
                diagram_accuracy
                < DecisionService.DIAGRAM_ACCURACY_THRESHOLD
            ):

                return {
                    "strategy": "diagram based",
                    "reason": (
                        f"The student's diagram-question "
                        f"accuracy is {diagram_accuracy:.1f}%, "
                        "which is below 50%. "
                        "A diagram-based strategy is selected."
                    ),
                    "score": latest_score,
                    "rule": "low_diagram_accuracy",
                    "diagram_accuracy": diagram_accuracy,
                }

        # ====================================================
        # RULE 4
        # DEFAULT
        # ====================================================

        return {
            "strategy": DecisionService.DEFAULT_STRATEGY,
            "reason": (
                "The student's performance does not trigger "
                "a specific adaptive rule. Using the default "
                "story-based teaching strategy."
            ),
            "score": latest_score,
            "rule": "default",
        }