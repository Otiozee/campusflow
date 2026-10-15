import unittest
from campusflownext.understanding_check import (
    QUESTION_BANK,
    calculate_score,
    validate_answer,
    get_question_text,
    get_correct_answer,
    get_explanation
)


class TestUnderstandingCheck(unittest.TestCase):
   
    def test_question_bank_has_six_questions(self):
        """Question bank has exactly 6 questions"""
        self.assertEqual(len(QUESTION_BANK), 6)
   
    def test_each_question_has_four_options(self):
        """Each question has exactly 4 options"""
        for q in QUESTION_BANK:
            self.assertEqual(len(q["options"]), 4)
   
    def test_each_question_has_valid_correct_answer(self):
        """Each question has a valid correct answer (A-D)"""
        for q in QUESTION_BANK:
            self.assertIn(q["correct"], ["A", "B", "C", "D"])
   
    def test_calculate_score_all_correct(self):
        """All correct answers gives score 6"""
        answers = [q["correct"] for q in QUESTION_BANK]
        score = calculate_score(answers)
        self.assertEqual(score, 6)
   
    def test_calculate_score_all_wrong(self):
        """All wrong answers gives score 0"""
        answers = ["A", "A", "A", "A", "A", "A"]
        # Make sure at least one is wrong
        for i, q in enumerate(QUESTION_BANK):
            if q["correct"] == "A":
                answers[i] = "B"
        score = calculate_score(answers)
        self.assertEqual(score, 0)
   
    def test_calculate_score_partial(self):
        """Partial correct answers gives partial score"""
        answers = []
        for i, q in enumerate(QUESTION_BANK):
            if i % 2 == 0:
                answers.append(q["correct"])  # Correct
            else:
                # Wrong answer
                wrong = "A"
                if q["correct"] == "A":
                    wrong = "B"
                answers.append(wrong)
       
        score = calculate_score(answers)
        self.assertEqual(score, 3)  # 3 correct out of 6
   
    def test_validate_answer_valid(self):
        """Valid answers pass validation"""
        self.assertTrue(validate_answer("A"))
        self.assertTrue(validate_answer("b"))
        self.assertTrue(validate_answer(" C "))
   
    def test_validate_answer_invalid(self):
        """Invalid answers fail validation"""
        self.assertFalse(validate_answer("E"))
        self.assertFalse(validate_answer(""))
        self.assertFalse(validate_answer("1"))
        self.assertFalse(validate_answer(None))
   
    def test_get_question_text(self):
        """Get question text returns string with question and options"""
        text = get_question_text(0)
        self.assertIn("Q1", text)
        self.assertIn("A.", text)
        self.assertIn("B.", text)
   
    def test_get_question_text_invalid_index(self):
        """Invalid index returns error message"""
        text = get_question_text(99)
        self.assertIn("Invalid", text)
   
    def test_get_correct_answer(self):
        """Get correct answer for question"""
        answer = get_correct_answer(0)
        self.assertEqual(answer, QUESTION_BANK[0]["correct"])
   
    def test_get_correct_answer_invalid_index(self):
        """Invalid index returns None"""
        answer = get_correct_answer(99)
        self.assertIsNone(answer)
   
    def test_get_explanation(self):
        """Get explanation for question"""
        explanation = get_explanation(0)
        self.assertIsInstance(explanation, str)
        self.assertGreater(len(explanation), 0)
   
    def test_get_explanation_invalid_index(self):
        """Invalid index returns error message"""
        explanation = get_explanation(99)
        self.assertIn("No explanation", explanation)


if __name__ == "__main__":
    unittest.main()

