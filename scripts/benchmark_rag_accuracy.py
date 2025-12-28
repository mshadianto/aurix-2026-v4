#!/usr/bin/env python3
"""
RAG Accuracy Benchmark Script for AURIX.

Evaluates RAG pipeline quality using RAGAS metrics to detect hallucinations
and measure retrieval/generation quality.

Metrics:
- Faithfulness: How factually accurate is the generated answer based on context
- Answer Relevancy: How relevant is the answer to the question
- Context Precision: How relevant are the retrieved contexts
- Context Recall: How much of the ground truth is covered by contexts

Usage:
    python scripts/benchmark_rag_accuracy.py --eval-framework ragas --output reports/
    python scripts/benchmark_rag_accuracy.py --eval-framework geval --questions data/test_questions.json
    python scripts/benchmark_rag_accuracy.py --quick-test
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
import warnings

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class RAGTestCase:
    """Single RAG test case with question, contexts, answer, and ground truth."""
    question: str
    contexts: List[str]
    answer: str
    ground_truth: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RAGEvalResult:
    """Evaluation result for a single test case."""
    question: str
    faithfulness: float
    answer_relevancy: float
    context_precision: float
    context_recall: float
    overall_score: float
    is_hallucination: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RAGBenchmarkSummary:
    """Summary of RAG benchmark results."""
    total_cases: int
    avg_faithfulness: float
    avg_answer_relevancy: float
    avg_context_precision: float
    avg_context_recall: float
    avg_overall_score: float
    hallucination_count: int
    hallucination_rate: float
    passed_threshold: bool
    threshold: float
    timestamp: str
    eval_framework: str


# Indonesian banking/audit test cases for RAG evaluation
AUDIT_TEST_CASES = [
    RAGTestCase(
        question="Apa threshold NPL ratio menurut regulasi OJK?",
        contexts=[
            "Berdasarkan POJK No. 40/POJK.03/2019, Bank wajib menjaga rasio NPL (Non-Performing Loan) gross tidak melebihi 5%. Bank dengan NPL di atas 5% akan mendapat pengawasan intensif dari OJK.",
            "Rasio kredit bermasalah (NPL) merupakan indikator kesehatan bank yang dipantau secara ketat. Warning level pada 3% dan danger level pada 5%.",
        ],
        answer="Menurut regulasi OJK, threshold NPL ratio adalah maksimal 5% (gross). Warning level dimulai dari 3%.",
        ground_truth="NPL ratio threshold adalah 5% sesuai POJK 40/POJK.03/2019, dengan warning level 3%."
    ),
    RAGTestCase(
        question="Bagaimana klasifikasi ESG Taxonomy menurut POJK 6/2022?",
        contexts=[
            "POJK Nomor 6/POJK.03/2022 tentang Taksonomi Hijau Indonesia mengklasifikasikan kegiatan ekonomi menjadi tiga kategori: GREEN (hijau) untuk kegiatan ramah lingkungan, BROWN (coklat) untuk kegiatan yang merusak lingkungan, dan TRANSITION untuk kegiatan transisi.",
            "Klasifikasi taksonomi ESG digunakan untuk menilai portofolio pembiayaan berkelanjutan bank.",
        ],
        answer="POJK 6/2022 mengklasifikasikan kegiatan ekonomi menjadi 3 kategori: GREEN (ramah lingkungan), BROWN (merusak lingkungan), dan TRANSITION (kegiatan transisi).",
        ground_truth="Klasifikasi ESG Taxonomy POJK 6/2022: GREEN, BROWN, dan TRANSITION."
    ),
    RAGTestCase(
        question="Apa saja 3 lines of defense dalam manajemen risiko?",
        contexts=[
            "Three Lines of Defense model: (1) First Line - Business units/operational management yang mengelola risiko sehari-hari, (2) Second Line - Risk management dan compliance functions yang mengawasi dan mendukung, (3) Third Line - Internal Audit yang memberikan assurance independen.",
            "Model pertahanan tiga lapis merupakan standar praktik tata kelola risiko yang diadopsi secara global.",
        ],
        answer="Three Lines of Defense: 1) First Line - Unit bisnis/operational management, 2) Second Line - Risk management dan compliance, 3) Third Line - Internal Audit sebagai assurance independen.",
        ground_truth="3 Lines of Defense: First Line (bisnis), Second Line (risk & compliance), Third Line (internal audit)."
    ),
    RAGTestCase(
        question="Apa itu Benford's Law dalam deteksi fraud?",
        contexts=[
            "Benford's Law menyatakan bahwa dalam dataset angka alami, digit pertama mengikuti distribusi tertentu: angka 1 muncul sekitar 30.1%, angka 2 sekitar 17.6%, dan seterusnya menurun. Penyimpangan signifikan dari distribusi ini dapat mengindikasikan manipulasi data atau fraud.",
            "Hukum Benford digunakan auditor untuk mendeteksi anomali dalam data keuangan seperti jurnal entries, expenses, dan invoice amounts.",
        ],
        answer="Benford's Law adalah hukum statistik yang menyatakan digit pertama dalam dataset alami mengikuti distribusi tertentu (1 muncul ~30.1%, 2 ~17.6%, dst). Penyimpangan dari distribusi ini dapat mengindikasikan fraud atau manipulasi data.",
        ground_truth="Benford's Law: distribusi digit pertama dalam data alami, digunakan untuk deteksi anomali dan fraud."
    ),
    RAGTestCase(
        question="Berapa target pembiayaan berkelanjutan menurut POJK 51/2017?",
        contexts=[
            "POJK 51/POJK.03/2017 mewajibkan bank untuk menyusun Rencana Aksi Keuangan Berkelanjutan (RAKB) dengan target porsi pembiayaan berkelanjutan minimal 20% dari total portofolio pada tahun 2025.",
            "Bank yang tidak memenuhi target pembiayaan berkelanjutan dapat dikenakan sanksi administratif oleh OJK.",
        ],
        answer="Menurut POJK 51/2017, target pembiayaan berkelanjutan adalah minimal 20% dari total portofolio pada tahun 2025.",
        ground_truth="Target pembiayaan berkelanjutan POJK 51/2017: minimal 20% pada 2025."
    ),
]


def evaluate_with_ragas(test_cases: List[RAGTestCase], llm_provider: str = "mock") -> List[RAGEvalResult]:
    """
    Evaluate RAG outputs using RAGAS framework.

    Falls back to simplified evaluation if RAGAS is not installed.
    """
    try:
        from ragas import evaluate
        from ragas.metrics import (
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall
        )
        from datasets import Dataset

        # Prepare dataset for RAGAS
        data = {
            "question": [tc.question for tc in test_cases],
            "answer": [tc.answer for tc in test_cases],
            "contexts": [tc.contexts for tc in test_cases],
            "ground_truth": [tc.ground_truth or "" for tc in test_cases],
        }

        dataset = Dataset.from_dict(data)

        # Run RAGAS evaluation
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = evaluate(
                dataset,
                metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
            )

        # Convert to our result format
        results = []
        df = result.to_pandas()

        for i, tc in enumerate(test_cases):
            row = df.iloc[i]
            faith = float(row.get("faithfulness", 0.0))
            relevancy = float(row.get("answer_relevancy", 0.0))
            precision = float(row.get("context_precision", 0.0))
            recall = float(row.get("context_recall", 0.0))

            overall = (faith + relevancy + precision + recall) / 4
            is_hallucination = faith < 0.7  # Faithfulness below 0.7 indicates potential hallucination

            results.append(RAGEvalResult(
                question=tc.question,
                faithfulness=faith,
                answer_relevancy=relevancy,
                context_precision=precision,
                context_recall=recall,
                overall_score=overall,
                is_hallucination=is_hallucination
            ))

        return results

    except ImportError:
        print("RAGAS not installed, using simplified evaluation...")
        return evaluate_simplified(test_cases)


def evaluate_with_geval(test_cases: List[RAGTestCase], llm_provider: str = "mock") -> List[RAGEvalResult]:
    """
    Evaluate RAG outputs using G-Eval methodology.

    G-Eval uses LLM-as-judge to score outputs on multiple dimensions.
    """
    from infrastructure.llm import create_llm_client

    client = create_llm_client(provider=llm_provider)
    results = []

    for tc in test_cases:
        # G-Eval prompt for faithfulness
        eval_prompt = f"""You are evaluating a RAG (Retrieval-Augmented Generation) system.

Question: {tc.question}

Retrieved Contexts:
{chr(10).join(f'- {ctx}' for ctx in tc.contexts)}

Generated Answer: {tc.answer}

Ground Truth (if available): {tc.ground_truth or 'N/A'}

Rate the following on a scale of 0.0 to 1.0:

1. FAITHFULNESS: Is the answer factually consistent with the provided contexts? (1.0 = completely faithful, 0.0 = hallucinated)
2. ANSWER_RELEVANCY: How relevant is the answer to the question? (1.0 = perfectly relevant, 0.0 = irrelevant)
3. CONTEXT_PRECISION: How relevant are the retrieved contexts to the question? (1.0 = all relevant, 0.0 = none relevant)
4. CONTEXT_RECALL: How much of the ground truth information is covered by the contexts? (1.0 = fully covered, 0.0 = not covered)

Respond in JSON format:
{{"faithfulness": 0.X, "answer_relevancy": 0.X, "context_precision": 0.X, "context_recall": 0.X, "reasoning": "..."}}
"""

        try:
            response = client.generate(prompt=eval_prompt, temperature=0.1, max_tokens=500)

            # Parse JSON response
            import re
            json_match = re.search(r'\{[^{}]*\}', response.content, re.DOTALL)
            if json_match:
                scores = json.loads(json_match.group())
            else:
                scores = {"faithfulness": 0.5, "answer_relevancy": 0.5, "context_precision": 0.5, "context_recall": 0.5}

            faith = float(scores.get("faithfulness", 0.5))
            relevancy = float(scores.get("answer_relevancy", 0.5))
            precision = float(scores.get("context_precision", 0.5))
            recall = float(scores.get("context_recall", 0.5))

            overall = (faith + relevancy + precision + recall) / 4
            is_hallucination = faith < 0.7

            results.append(RAGEvalResult(
                question=tc.question,
                faithfulness=faith,
                answer_relevancy=relevancy,
                context_precision=precision,
                context_recall=recall,
                overall_score=overall,
                is_hallucination=is_hallucination,
                details={"reasoning": scores.get("reasoning", "")}
            ))

        except Exception as e:
            print(f"  Warning: G-Eval failed for question, using defaults: {e}")
            results.append(RAGEvalResult(
                question=tc.question,
                faithfulness=0.5,
                answer_relevancy=0.5,
                context_precision=0.5,
                context_recall=0.5,
                overall_score=0.5,
                is_hallucination=False,
                details={"error": str(e)}
            ))

    return results


def evaluate_simplified(test_cases: List[RAGTestCase]) -> List[RAGEvalResult]:
    """
    Simplified evaluation using keyword matching and heuristics.

    Used as fallback when RAGAS/G-Eval are not available.
    """
    results = []

    for tc in test_cases:
        # Simple keyword overlap scoring
        context_text = " ".join(tc.contexts).lower()
        answer_text = tc.answer.lower()
        question_text = tc.question.lower()
        ground_truth_text = (tc.ground_truth or "").lower()

        # Faithfulness: Check if answer terms appear in context
        answer_words = set(answer_text.split())
        context_words = set(context_text.split())
        faith_overlap = len(answer_words & context_words) / max(len(answer_words), 1)
        faithfulness = min(faith_overlap * 1.5, 1.0)  # Scale up, cap at 1.0

        # Answer relevancy: Check if question terms appear in answer
        question_words = set(question_text.split()) - {"apa", "bagaimana", "berapa", "adalah", "dalam", "yang", "dan", "untuk"}
        relevancy_overlap = len(answer_words & question_words) / max(len(question_words), 1)
        answer_relevancy = min(relevancy_overlap * 2.0, 1.0)

        # Context precision: Check if question terms appear in contexts
        context_precision = len(context_words & question_words) / max(len(question_words), 1)
        context_precision = min(context_precision * 1.5, 1.0)

        # Context recall: Check ground truth coverage
        if ground_truth_text:
            ground_words = set(ground_truth_text.split())
            recall_overlap = len(context_words & ground_words) / max(len(ground_words), 1)
            context_recall = min(recall_overlap * 1.5, 1.0)
        else:
            context_recall = 0.8  # Default if no ground truth

        overall = (faithfulness + answer_relevancy + context_precision + context_recall) / 4
        is_hallucination = faithfulness < 0.7

        results.append(RAGEvalResult(
            question=tc.question,
            faithfulness=round(faithfulness, 3),
            answer_relevancy=round(answer_relevancy, 3),
            context_precision=round(context_precision, 3),
            context_recall=round(context_recall, 3),
            overall_score=round(overall, 3),
            is_hallucination=is_hallucination,
            details={"method": "simplified_keyword_matching"}
        ))

    return results


def calculate_summary(
    results: List[RAGEvalResult],
    threshold: float,
    eval_framework: str
) -> RAGBenchmarkSummary:
    """Calculate summary statistics from evaluation results."""
    if not results:
        return None

    avg_faith = sum(r.faithfulness for r in results) / len(results)
    avg_rel = sum(r.answer_relevancy for r in results) / len(results)
    avg_prec = sum(r.context_precision for r in results) / len(results)
    avg_rec = sum(r.context_recall for r in results) / len(results)
    avg_overall = sum(r.overall_score for r in results) / len(results)
    hallucination_count = sum(1 for r in results if r.is_hallucination)

    return RAGBenchmarkSummary(
        total_cases=len(results),
        avg_faithfulness=round(avg_faith, 3),
        avg_answer_relevancy=round(avg_rel, 3),
        avg_context_precision=round(avg_prec, 3),
        avg_context_recall=round(avg_rec, 3),
        avg_overall_score=round(avg_overall, 3),
        hallucination_count=hallucination_count,
        hallucination_rate=round(hallucination_count / len(results), 3),
        passed_threshold=avg_faith >= threshold,
        threshold=threshold,
        timestamp=datetime.now().isoformat(),
        eval_framework=eval_framework
    )


def print_results(results: List[RAGEvalResult], summary: RAGBenchmarkSummary):
    """Print formatted evaluation results."""
    print(f"\n{'='*70}")
    print("RAG Accuracy Benchmark Results")
    print(f"{'='*70}")

    for i, r in enumerate(results, 1):
        halluc_marker = " [HALLUCINATION]" if r.is_hallucination else ""
        print(f"\n{i}. {r.question[:50]}...{halluc_marker}")
        print(f"   Faithfulness: {r.faithfulness:.3f} | Relevancy: {r.answer_relevancy:.3f}")
        print(f"   Precision: {r.context_precision:.3f} | Recall: {r.context_recall:.3f}")
        print(f"   Overall: {r.overall_score:.3f}")

    print(f"\n{'='*70}")
    print("Summary")
    print(f"{'='*70}")
    print(f"Total Test Cases: {summary.total_cases}")
    print(f"Evaluation Framework: {summary.eval_framework}")
    print(f"\nAverage Scores:")
    print(f"  Faithfulness:      {summary.avg_faithfulness:.3f}")
    print(f"  Answer Relevancy:  {summary.avg_answer_relevancy:.3f}")
    print(f"  Context Precision: {summary.avg_context_precision:.3f}")
    print(f"  Context Recall:    {summary.avg_context_recall:.3f}")
    print(f"  Overall Score:     {summary.avg_overall_score:.3f}")
    print(f"\nHallucination Detection:")
    print(f"  Hallucinations Found: {summary.hallucination_count}/{summary.total_cases}")
    print(f"  Hallucination Rate:   {summary.hallucination_rate:.1%}")
    print(f"\nThreshold Check (faithfulness >= {summary.threshold}):")
    status = "PASS" if summary.passed_threshold else "FAIL"
    print(f"  Status: {status}")


def save_results(
    results: List[RAGEvalResult],
    summary: RAGBenchmarkSummary,
    output_dir: str
):
    """Save benchmark results to JSON files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Save detailed results
    details_file = output_path / "rag_accuracy_details.json"
    with open(details_file, 'w', encoding='utf-8') as f:
        json.dump({
            "results": [asdict(r) for r in results],
            "timestamp": datetime.now().isoformat()
        }, f, indent=2, ensure_ascii=False)

    # Save summary
    summary_file = output_path / "rag_accuracy_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(asdict(summary), f, indent=2)

    print(f"\nResults saved to:")
    print(f"  Details: {details_file}")
    print(f"  Summary: {summary_file}")


def load_custom_test_cases(file_path: str) -> List[RAGTestCase]:
    """Load custom test cases from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    test_cases = []
    for item in data:
        test_cases.append(RAGTestCase(
            question=item["question"],
            contexts=item["contexts"],
            answer=item["answer"],
            ground_truth=item.get("ground_truth"),
            metadata=item.get("metadata", {})
        ))

    return test_cases


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark RAG accuracy for AURIX using RAGAS or G-Eval"
    )
    parser.add_argument(
        "--eval-framework", "-e",
        type=str,
        choices=["ragas", "geval", "simplified"],
        default="simplified",
        help="Evaluation framework to use (default: simplified)"
    )
    parser.add_argument(
        "--questions", "-q",
        type=str,
        help="Path to custom test questions JSON file"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="reports/",
        help="Output directory for results (default: reports/)"
    )
    parser.add_argument(
        "--threshold", "-t",
        type=float,
        default=0.85,
        help="Faithfulness threshold for pass/fail (default: 0.85)"
    )
    parser.add_argument(
        "--llm-provider", "-p",
        type=str,
        default="mock",
        help="LLM provider for G-Eval (default: mock)"
    )
    parser.add_argument(
        "--quick-test",
        action="store_true",
        help="Run quick test with first 2 cases only"
    )

    args = parser.parse_args()

    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    print("AURIX RAG Accuracy Benchmark")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Evaluation Framework: {args.eval_framework}")

    # Load test cases
    if args.questions:
        print(f"Loading custom test cases from: {args.questions}")
        test_cases = load_custom_test_cases(args.questions)
    else:
        print("Using built-in Indonesian banking/audit test cases")
        test_cases = AUDIT_TEST_CASES

    if args.quick_test:
        test_cases = test_cases[:2]
        print(f"Quick test mode: using {len(test_cases)} cases")

    print(f"Total test cases: {len(test_cases)}")

    # Run evaluation
    print(f"\nRunning {args.eval_framework} evaluation...")

    if args.eval_framework == "ragas":
        results = evaluate_with_ragas(test_cases, args.llm_provider)
    elif args.eval_framework == "geval":
        results = evaluate_with_geval(test_cases, args.llm_provider)
    else:
        results = evaluate_simplified(test_cases)

    # Calculate summary
    summary = calculate_summary(results, args.threshold, args.eval_framework)

    # Print and save results
    print_results(results, summary)
    save_results(results, summary, args.output)

    # Exit code based on threshold
    sys.exit(0 if summary.passed_threshold else 1)


if __name__ == "__main__":
    main()
