"""
AI assistant module for answering questions about meetings.
Supports both Claude (Anthropic) and ChatGPT (OpenAI).
"""
import os
from anthropic import Anthropic
from openai import OpenAI


class AIAssistant:
    """AI assistant for answering questions based on meeting transcripts."""

    def __init__(self, provider="claude", anthropic_key=None, openai_key=None):
        """
        Initialize the AI assistant.

        Args:
            provider: "claude" or "chatgpt"
            anthropic_key: Anthropic API key (for Claude)
            openai_key: OpenAI API key (for ChatGPT)
        """
        self.provider = provider.lower()

        if self.provider == "claude":
            self.anthropic_key = anthropic_key or os.getenv("ANTHROPIC_API_KEY")
            if not self.anthropic_key:
                raise ValueError("Anthropic API key not provided")
            self.client = Anthropic(api_key=self.anthropic_key)
            self.model = "claude-3-5-sonnet-20241022"

        elif self.provider == "chatgpt":
            self.openai_key = openai_key or os.getenv("OPENAI_API_KEY")
            if not self.openai_key:
                raise ValueError("OpenAI API key not provided")
            self.client = OpenAI(api_key=self.openai_key)
            self.model = "gpt-4o"

        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'claude' or 'chatgpt'")

        self.conversation_history = []

    def prepare_answer(self, question, transcript, context=None):
        """
        Generate an answer to a question based on the meeting transcript.

        Args:
            question: The question to answer
            transcript: The meeting transcript
            context: Optional additional context

        Returns:
            str: The AI-generated answer
        """
        # Build the prompt
        system_prompt = """You are an intelligent assistant helping with meeting analysis.
Your task is to answer questions based on the provided meeting transcript.
Provide clear, concise, and accurate answers. If the information is not in the transcript,
clearly state that."""

        user_prompt = f"""Meeting Transcript:
{transcript}

{f"Additional Context: {context}" if context else ""}

Question: {question}

Please provide a detailed answer based on the meeting transcript."""

        try:
            if self.provider == "claude":
                return self._ask_claude(system_prompt, user_prompt)
            else:
                return self._ask_chatgpt(system_prompt, user_prompt)

        except Exception as e:
            print(f"Error generating answer: {e}")
            raise

    def _ask_claude(self, system_prompt, user_prompt):
        """Ask Claude for an answer."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.content[0].text

    def _ask_chatgpt(self, system_prompt, user_prompt):
        """Ask ChatGPT for an answer."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=2048
        )
        return response.choices[0].message.content

    def interactive_qa(self, transcript):
        """
        Start an interactive Q&A session about the transcript.

        Args:
            transcript: The meeting transcript
        """
        print("\n" + "=" * 80)
        print("INTERACTIVE Q&A SESSION")
        print("=" * 80)
        print(f"Using AI Provider: {self.provider.upper()}")
        print("Ask questions about the meeting. Type 'exit' or 'quit' to end.\n")

        while True:
            question = input("\nYour Question: ").strip()

            if question.lower() in ['exit', 'quit', 'q']:
                print("Ending Q&A session.")
                break

            if not question:
                print("Please enter a question.")
                continue

            print(f"\n[{self.provider.upper()} is thinking...]")

            try:
                answer = self.prepare_answer(question, transcript)
                print(f"\n{self.provider.upper()} Answer:")
                print("-" * 80)
                print(answer)
                print("-" * 80)

            except Exception as e:
                print(f"\nError: {e}")
                print("Please try again.")

    def generate_summary(self, transcript):
        """
        Generate a summary of the meeting.

        Args:
            transcript: The meeting transcript

        Returns:
            str: Meeting summary
        """
        prompt = """Please provide a comprehensive summary of this meeting transcript.
Include:
1. Main topics discussed
2. Key decisions made
3. Action items (if any)
4. Important points or takeaways

Meeting Transcript:
""" + transcript

        system_prompt = "You are an expert at summarizing meetings and extracting key information."

        try:
            if self.provider == "claude":
                return self._ask_claude(system_prompt, prompt)
            else:
                return self._ask_chatgpt(system_prompt, prompt)

        except Exception as e:
            print(f"Error generating summary: {e}")
            raise

    def generate_interview_prep(self, transcript):
        """
        Generate interview preparation materials based on the meeting/interview.

        Args:
            transcript: The interview/meeting transcript

        Returns:
            str: Interview preparation guide
        """
        prompt = """Based on this interview/meeting transcript, please generate:

1. Key questions that were asked
2. Recommended answers or talking points for each question
3. Areas that might need more preparation
4. Overall assessment and tips

Interview/Meeting Transcript:
""" + transcript

        system_prompt = """You are an expert career coach and interview preparation specialist.
Provide actionable, specific advice."""

        try:
            if self.provider == "claude":
                return self._ask_claude(system_prompt, prompt)
            else:
                return self._ask_chatgpt(system_prompt, prompt)

        except Exception as e:
            print(f"Error generating interview prep: {e}")
            raise

    def extract_questions_and_answers(self, transcript):
        """
        Extract questions and generate good answers from a meeting transcript.

        Args:
            transcript: The meeting transcript

        Returns:
            str: Formatted Q&A document
        """
        prompt = """Analyze this meeting/interview transcript and:

1. Identify all questions that were asked
2. For each question, provide a well-structured, professional answer
3. If answers were already given in the transcript, improve them
4. If questions weren't fully answered, provide complete answers

Format the output as:
Q1: [Question]
A1: [Detailed Answer]

Q2: [Question]
A2: [Detailed Answer]

Transcript:
""" + transcript

        system_prompt = """You are an expert communicator who excels at formulating
clear, professional answers to questions. Provide thoughtful, complete responses."""

        try:
            if self.provider == "claude":
                return self._ask_claude(system_prompt, prompt)
            else:
                return self._ask_chatgpt(system_prompt, prompt)

        except Exception as e:
            print(f"Error extracting Q&A: {e}")
            raise

    def generate_star_answer(self, question, transcript, format_type="full"):
        """
        Generate an answer in STAR format (Situation, Task, Action, Result).

        Args:
            question: The question to answer
            transcript: The meeting/interview transcript
            format_type: "full" for complete sentences or "bullets" for bullet points

        Returns:
            dict: STAR formatted answer with components
        """
        if format_type == "bullets":
            prompt = f"""Based on this transcript, answer the following question using the STAR format.
Provide your answer in CONCISE bullet points.

Question: {question}

Format your response as:
**Situation:**
- [Key point about the situation]
- [Additional context if needed]

**Task:**
- [What needed to be accomplished]
- [Specific objectives]

**Action:**
- [Specific action taken]
- [Steps involved]
- [Methods used]

**Result:**
- [Measurable outcome]
- [Impact achieved]

Transcript:
{transcript}

Provide a brief, focused STAR answer based on the information available."""

        else:  # full format
            prompt = f"""Based on this transcript, answer the following question using the STAR format.
Provide your answer in complete, professional sentences.

Question: {question}

Format your response as:
**Situation:** [Describe the context and background in 2-3 sentences]

**Task:** [Explain what needed to be accomplished in 1-2 sentences]

**Action:** [Detail the specific actions taken in 2-4 sentences]

**Result:** [Describe the outcome and impact in 2-3 sentences]

Transcript:
{transcript}

Provide a comprehensive STAR answer based on the information available."""

        system_prompt = """You are an expert interview coach specializing in STAR method responses.
Create compelling, structured answers that demonstrate clear problem-solving and results."""

        try:
            if self.provider == "claude":
                response = self._ask_claude(system_prompt, prompt)
            else:
                response = self._ask_chatgpt(system_prompt, prompt)

            # Parse the response into components
            components = self._parse_star_response(response)
            return {
                "full_response": response,
                "components": components,
                "format_type": format_type
            }

        except Exception as e:
            print(f"Error generating STAR answer: {e}")
            raise

    def _parse_star_response(self, response):
        """Parse STAR response into components."""
        components = {
            "situation": "",
            "task": "",
            "action": "",
            "result": ""
        }

        lines = response.split("\n")
        current_section = None

        for line in lines:
            line_lower = line.lower().strip()
            if line_lower.startswith("**situation"):
                current_section = "situation"
                # Extract content after the header if present
                if ":" in line:
                    content = line.split(":", 1)[1].strip()
                    if content and not content.startswith("**"):
                        components[current_section] += content + "\n"
            elif line_lower.startswith("**task"):
                current_section = "task"
                if ":" in line:
                    content = line.split(":", 1)[1].strip()
                    if content and not content.startswith("**"):
                        components[current_section] += content + "\n"
            elif line_lower.startswith("**action"):
                current_section = "action"
                if ":" in line:
                    content = line.split(":", 1)[1].strip()
                    if content and not content.startswith("**"):
                        components[current_section] += content + "\n"
            elif line_lower.startswith("**result"):
                current_section = "result"
                if ":" in line:
                    content = line.split(":", 1)[1].strip()
                    if content and not content.startswith("**"):
                        components[current_section] += content + "\n"
            elif current_section and line.strip() and not line.strip().startswith("**"):
                components[current_section] += line.strip() + "\n"

        # Clean up whitespace
        for key in components:
            components[key] = components[key].strip()

        return components

    def quick_answer(self, question, transcript, format_type="bullets"):
        """
        Generate a quick answer optimized for speed.

        Args:
            question: The question to answer
            transcript: The transcript (can be partial)
            format_type: "bullets" or "full"

        Returns:
            str: Quick answer
        """
        # For quick answers, we use a simpler prompt and lower max_tokens
        if format_type == "bullets":
            prompt = f"""Question: {question}

Based on this transcript excerpt, provide a brief STAR format answer in bullet points.

Transcript:
{transcript[:3000]}  # Limit to first 3000 chars for speed

Be concise and focus on key points only."""
        else:
            prompt = f"""Question: {question}

Based on this transcript excerpt, provide a STAR format answer in 2-3 sentences per section.

Transcript:
{transcript[:3000]}

Be concise and professional."""

        system_prompt = "Provide concise, focused STAR format answers quickly."

        try:
            if self.provider == "claude":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,  # Reduced for speed
                    system=system_prompt,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1024  # Reduced for speed
                )
                return response.choices[0].message.content

        except Exception as e:
            print(f"Error generating quick answer: {e}")
            raise
