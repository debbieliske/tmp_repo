import pandas as pd
import matplotlib.pyplot as plt

def calculate_statistics(df):
    """Calculate key statistics for the report."""
    # Unique repositories
    unique_repos = df[['Repository Name']].drop_duplicates()
    total_repos = len(unique_repos)

    # Total repo-branches
    total_repo_branches = len(df)

    # Repo-branches with perfect scores
    perfect_score_repo_branches = df[(df.iloc[:, 2:] == 'Passed').all(axis=1)]
    perfect_score_repos = perfect_score_repo_branches[['Repository Name']].drop_duplicates()

    # Most common failed tests
    all_failures = df.iloc[:, 2:].stack()[df.iloc[:, 2:].stack() == 'Failed']
    failure_counts = all_failures.groupby(level=1).size().sort_values(ascending=False)
    failure_percentages = (failure_counts / total_repo_branches * 100).round(2)

    # Add Failure Count for each repo-branch
    df['Failure Count'] = (df.iloc[:, 2:] == 'Failed').sum(axis=1)

    # Top 5 repositories with most failures (unique repositories)
    repo_failure_totals = df.groupby('Repository Name').agg(
        total_failures=('Failure Count', 'sum'),
        branch_count=('default branch', 'count')
    ).sort_values(by='total_failures', ascending=False).head(5)

    return {
        'total_repos': total_repos,
        'total_repo_branches': total_repo_branches,
        'perfect_score_repo_branches': perfect_score_repo_branches,
        'perfect_score_repos': perfect_score_repos,
        'failure_counts': failure_counts,
        'failure_percentages': failure_percentages,
        'repo_failure_totals': repo_failure_totals
    }

def generate_plots(df, failure_counts):
    """Generate plots for the report."""
    plt.figure(figsize=(10, 6))
    failure_counts.plot(kind='bar', color='red')
    plt.title('Most Common Failed Tests')
    plt.ylabel('Number of Failures')
    plt.xlabel('Test')
    plt.tight_layout()
    plt.savefig("failure_counts_plot.png")
    plt.close()

    plt.figure(figsize=(10, 6))
    df['Failure Count'].value_counts().sort_index().plot(kind='bar', color='blue')
    plt.title('Distribution of Failure Counts Across Repo-Branches')
    plt.ylabel('Number of Repo-Branches')
    plt.xlabel('Failure Count')
    plt.tight_layout()
    plt.savefig("failure_distribution_plot.png")
    plt.close()

def generate_markdown_report(df, stats):
    """Generate a Markdown report using the calculated statistics."""
    markdown = []
    markdown.append("# Repository Analysis Report\n")

    # High-Level Statistics
    markdown.append("## High-Level Statistics\n")
    markdown.append(f"- **Total unique repositories analyzed**: {stats['total_repos']}")
    markdown.append(f"- **Total repo-branches analyzed**: {stats['total_repo_branches']}")
    markdown.append(f"- **Repositories passing all tests**: {len(stats['perfect_score_repos'])}")
    markdown.append(f"- **Repo-branches passing all tests**: {len(stats['perfect_score_repo_branches'])}\n")

    # Perfect Scores
    markdown.append("## Repositories with Perfect Scores\n")
    if not stats['perfect_score_repos'].empty:
        for repo in stats['perfect_score_repos']['Repository Name']:
            markdown.append(f"- **{repo}**")
    else:
        markdown.append("- None")
    markdown.append("")

    markdown.append("## Repo-Branches with Perfect Scores\n")
    if not stats['perfect_score_repo_branches'].empty:
        for _, row in stats['perfect_score_repo_branches'].iterrows():
            markdown.append(f"- **{row['Repository Name']} ({row['default branch']})**")
    else:
        markdown.append("- None")
    markdown.append("")

    # Most Common Failed Tests
    markdown.append("## Most Common Failed Tests\n")
    markdown.append("| Test Name | Failures | Failure Percentage |")
    markdown.append("|-----------|----------|--------------------|")
    for test, count in stats['failure_counts'].items():
        percentage = stats['failure_percentages'][test]
        markdown.append(f"| {test} | {count} | {percentage}% |")
    markdown.append("")

    # Top 5 Repositories with Most Failures
    markdown.append("## Top 5 Repositories with Most Failures\n")
    markdown.append("| Repository Name | Total Failures | Number of Branches |")
    markdown.append("|-----------------|----------------|---------------------|")
    for repo, row in stats['repo_failure_totals'].iterrows():
        markdown.append(f"| {repo} | {row['total_failures']} | {row['branch_count']} |")
    markdown.append("")

    # Add Plot Links
    markdown.append("## Visualizations\n")
    markdown.append("![Most Common Failed Tests](failure_counts_plot.png)")
    markdown.append("![Failure Distribution Across Repo-Branches](failure_distribution_plot.png)")
    markdown.append("")

    # Detailed Repository Results
    markdown.append("## Detailed Repository Results\n")
    markdown.append("| Repository Name | Default Branch | " + " | ".join(df.columns[2:]) + " |")
    markdown.append("|-----------------|----------------|" + "|".join(["---"] * (len(df.columns) - 2)) + "|")

    for _, row in df.iterrows():
        row_data = []
        for col in df.columns[2:]:
            value = str(row[col])  # Ensure all values are strings
            if value == 'Failed':
                row_data.append(f"<span style='background-color: lightcoral'>{value}</span>")
            else:
                row_data.append(value)
        markdown.append(f"| {row['Repository Name']} | {row['default branch']} | " + " | ".join(row_data) + " |")

    # Save the Markdown report
    with open("repo_results_report.md", "w") as f:
        f.write("\n".join(markdown))

    print("Markdown report generated: repo_results_report.md")

# Easy to remove CSV reading code
try:
    repo_results = pd.read_csv("repo_results.csv")
except FileNotFoundError:
    print("CSV file not found. Please provide the 'repo_results.csv' file or replace with your DataFrame loading logic.")
    repo_results = pd.DataFrame()  # Placeholder

if not repo_results.empty:
    stats = calculate_statistics(repo_results)
    generate_plots(repo_results, stats['failure_counts'])
    generate_markdown_report(repo_results, stats)
else:
    print("No data to generate report.")
