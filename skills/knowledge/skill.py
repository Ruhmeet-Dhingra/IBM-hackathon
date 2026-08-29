from brain_v2.models import Step
from brain_v2.entities import Action
from ai.rag import search_knowledge_base, answer_from_context

class KnowledgeSkill:
    """Skill to handle retrieval-augmented generation from local knowledge base."""
    
    def execute(self, step: Step) -> str:
        if step.action == Action.SEARCH_KNOWLEDGE_BASE:
            # We need the user's original query. Where is it?
            # Wait, the planner didn't pass the raw query! 
            # I need to get the query from the planner parameters.
            query = step.parameters.get("query", "") if step.parameters else ""
            if not query:
                return "I'm not sure what to search for in your notes."
                
            context = search_knowledge_base(query)
            answer = answer_from_context(query, context)
            return answer
        
        raise ValueError(f"KnowledgeSkill cannot handle action: {step.action}")
