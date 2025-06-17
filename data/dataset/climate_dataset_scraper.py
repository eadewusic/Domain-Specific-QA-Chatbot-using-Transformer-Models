import pandas as pd
import json
import os
import logging
from typing import List, Dict
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClimateDatasetBuilder:
    """
    Complete climate dataset builder that creates a comprehensive dataset from scratch
    """
    
    def __init__(self):
        self.dataset = []
        
    def create_base_dataset(self) -> List[Dict]:
        """
        Create the base comprehensive climate education dataset
        """
        dataset = []
        
        # BASIC CONCEPTS (40% of dataset)
        basic_concepts = [
            {
                'question': 'What is the greenhouse effect?',
                'answer': 'The greenhouse effect is a natural process where certain gases in Earth\'s atmosphere trap heat from the sun. When sunlight reaches Earth, some is reflected back to space, but most is absorbed by the surface. Earth then radiates this energy as heat. Greenhouse gases like carbon dioxide, methane, and water vapor absorb this heat and re-emit it in all directions, including back toward Earth. This process keeps Earth about 33°C warmer than it would be without these gases, making life possible.',
                'category': 'basic_concepts',
                'difficulty': 'beginner',
                'source': 'manual_curation'
            },
            {
                'question': 'What is the enhanced greenhouse effect?',
                'answer': 'The enhanced greenhouse effect occurs when human activities increase the concentration of greenhouse gases in the atmosphere beyond natural levels. This extra layer of greenhouse gases traps more heat than the natural greenhouse effect, causing global temperatures to rise. The main culprit is carbon dioxide from burning fossil fuels, which has increased atmospheric CO2 by over 40% since pre-industrial times.',
                'category': 'basic_concepts',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What is the difference between weather and climate?',
                'answer': 'Weather refers to short-term atmospheric conditions in a specific place at a specific time, such as temperature, precipitation, and wind on a particular day. Climate, however, describes the long-term average weather patterns in a region over decades or centuries. Think of it this way: climate is what you expect, weather is what you get. For example, you expect hot summers in Arizona (climate), but any single day might be cooler than average (weather).',
                'category': 'basic_concepts',
                'difficulty': 'beginner',
                'source': 'manual_curation'
            },
            {
                'question': 'What are the main greenhouse gases?',
                'answer': 'The main greenhouse gases are: 1) Carbon dioxide (CO2) - the most abundant, primarily from burning fossil fuels; 2) Methane (CH4) - from agriculture, landfills, and natural gas; 3) Nitrous oxide (N2O) - from fertilizers and fossil fuel combustion; 4) Fluorinated gases - from refrigeration and industrial processes; and 5) Water vapor (H2O) - increases as atmosphere warms. CO2 accounts for about 76% of total greenhouse gas emissions.',
                'category': 'basic_concepts',
                'difficulty': 'beginner',
                'source': 'manual_curation'
            },
            {
                'question': 'How do we know climate change is happening?',
                'answer': 'We know climate change is happening through multiple lines of evidence: 1) Temperature records show warming trends since the 1880s; 2) Ice core data reveals atmospheric CO2 levels are higher than any time in 800,000 years; 3) Glaciers and ice sheets are shrinking globally; 4) Sea levels are rising; 5) Ocean temperatures are increasing; 6) Seasonal patterns are shifting; and 7) Extreme weather events are becoming more frequent. This evidence comes from thousands of scientists worldwide using independent measurement methods.',
                'category': 'basic_concepts',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What is carbon dioxide and why is it important for climate?',
                'answer': 'Carbon dioxide (CO2) is a colorless, odorless gas that occurs naturally in Earth\'s atmosphere. It\'s crucial for climate because it\'s a greenhouse gas that traps heat. Plants use CO2 for photosynthesis, and animals produce it when breathing. However, human activities, especially burning fossil fuels, have increased atmospheric CO2 by over 40% since pre-industrial times. This extra CO2 enhances the greenhouse effect, causing global temperatures to rise.',
                'category': 'basic_concepts',
                'difficulty': 'beginner',
                'source': 'manual_curation'
            },
            {
                'question': 'What is the carbon cycle?',
                'answer': 'The carbon cycle is the process by which carbon moves between Earth\'s atmosphere, land, oceans, and living organisms. Carbon is exchanged through photosynthesis (plants absorb CO2), respiration (organisms release CO2), ocean absorption, volcanic emissions, and decomposition. Human activities have disrupted this natural cycle by adding extra CO2 through fossil fuel burning and deforestation, leading to more carbon in the atmosphere than natural processes can remove.',
                'category': 'basic_concepts',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What is global warming?',
                'answer': 'Global warming refers to the long-term increase in Earth\'s average surface temperature due to human activities and natural factors. Since the late 1800s, the average global temperature has risen by about 1.1°C (2°F), with most of this warming occurring in the past 40 years. The primary cause is increased greenhouse gas emissions from burning fossil fuels, which trap more heat in the atmosphere.',
                'category': 'basic_concepts',
                'difficulty': 'beginner',
                'source': 'manual_curation'
            },
            {
                'question': 'What is climate feedback?',
                'answer': 'Climate feedback occurs when changes in the climate system trigger additional changes that either amplify (positive feedback) or reduce (negative feedback) the original change. For example, as ice melts due to warming, it exposes darker surfaces that absorb more heat, causing more warming and melting - this is positive feedback. Cloud formation can provide negative feedback by reflecting sunlight back to space. Understanding feedbacks is crucial for predicting future climate changes.',
                'category': 'basic_concepts',
                'difficulty': 'advanced',
                'source': 'manual_curation'
            },
            {
                'question': 'What is the albedo effect?',
                'answer': 'The albedo effect refers to how much sunlight a surface reflects back to space. Light-colored surfaces like ice and snow have high albedo (reflect most sunlight), while dark surfaces like forests and oceans have low albedo (absorb most sunlight). As global warming melts ice and snow, it exposes darker surfaces underneath, which absorb more heat and cause additional warming. This creates a positive feedback loop that accelerates climate change.',
                'category': 'basic_concepts',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What are fossil fuels?',
                'answer': 'Fossil fuels are energy sources formed from the remains of ancient plants and animals buried and compressed over millions of years. The main types are coal, oil (petroleum), and natural gas. When burned for energy, fossil fuels release carbon dioxide and other greenhouse gases that were stored underground. This is the primary source of human-caused climate change, as we\'re essentially releasing millions of years worth of stored carbon back into the atmosphere in just a few centuries.',
                'category': 'basic_concepts',
                'difficulty': 'beginner',
                'source': 'manual_curation'
            },
            {
                'question': 'What is methane and why is it important for climate?',
                'answer': 'Methane (CH4) is a potent greenhouse gas that is about 25 times more effective at trapping heat than carbon dioxide over a 100-year period. It comes from natural sources like wetlands and human activities including agriculture (especially livestock), landfills, and natural gas production. While methane makes up a smaller percentage of total emissions than CO2, its high warming potential makes it a critical target for climate action. The good news is that methane breaks down faster in the atmosphere than CO2.',
                'category': 'basic_concepts',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
        ]
        
        # IMPACTS (25% of dataset)
        impacts = [
            {
                'question': 'How does climate change affect sea levels?',
                'answer': 'Climate change causes sea levels to rise through two main processes: thermal expansion and ice melting. As ocean water warms, it expands, taking up more space. Additionally, glaciers and ice sheets on land are melting, adding water to the oceans. Global sea levels have risen about 8-9 inches since 1880, with the rate of increase accelerating in recent decades. This threatens coastal communities, infrastructure, and ecosystems worldwide.',
                'category': 'impacts',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What are the health impacts of climate change?',
                'answer': 'Climate change affects human health in several ways: 1) Heat-related illnesses from extreme temperatures; 2) Air quality problems from increased pollution and wildfires; 3) Vector-borne diseases spreading to new areas as climates warm; 4) Food and water security issues; 5) Mental health impacts from extreme weather events; and 6) Displacement of communities. Vulnerable populations, including children, elderly, and those with pre-existing conditions, face the greatest risks.',
                'category': 'impacts',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'How does climate change affect wildlife and ecosystems?',
                'answer': 'Climate change impacts wildlife and ecosystems by altering habitats, food sources, and migration patterns. Rising temperatures force species to migrate to cooler areas or higher elevations. Changing precipitation affects water availability. Ocean acidification harms marine life with shells and skeletons. Timing mismatches occur when species\' life cycles no longer align with their food sources. Some species adapt, but many face extinction, leading to biodiversity loss and ecosystem disruption.',
                'category': 'impacts',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What is ocean acidification?',
                'answer': 'Ocean acidification occurs when the ocean absorbs excess carbon dioxide from the atmosphere, making seawater more acidic. The ocean has absorbed about 30% of human-produced CO2, which lowers the pH of seawater. This makes it harder for marine organisms like corals, shellfish, and some plankton to build their calcium carbonate shells and skeletons. Ocean acidification is sometimes called "the other CO2 problem" and threatens marine food webs.',
                'category': 'impacts',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'How does climate change affect extreme weather?',
                'answer': 'Climate change increases the frequency and intensity of extreme weather events. Warmer air holds more moisture, leading to heavier rainfall and flooding. Higher temperatures contribute to more severe droughts and heat waves. Warmer ocean temperatures fuel stronger hurricanes and typhoons. Changing atmospheric patterns can cause more persistent weather patterns, leading to prolonged droughts or extended periods of extreme heat.',
                'category': 'impacts',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'How does climate change affect agriculture?',
                'answer': 'Climate change affects agriculture through changing temperatures, precipitation patterns, and extreme weather events. Higher temperatures can stress crops and livestock, while changing rainfall patterns can lead to droughts or flooding. Some regions may see longer growing seasons, but increased heat, pests, and diseases often offset these benefits. Food security is threatened as crop yields become more unpredictable, and nutritional quality of some crops may decline due to higher CO2 levels.',
                'category': 'impacts',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What are climate tipping points?',
                'answer': 'Climate tipping points are thresholds in the climate system where small changes trigger large, often irreversible shifts. Examples include the collapse of ice sheets, shutdown of ocean currents, dieback of forests, or thawing of permafrost. Once crossed, these tipping points can lead to cascading effects and accelerated warming. Scientists have identified several potential tipping points that could be reached with 1.5-2°C of warming, making rapid emission reductions crucial.',
                'category': 'impacts',
                'difficulty': 'advanced',
                'source': 'manual_curation'
            },
            {
                'question': 'How does climate change affect water resources?',
                'answer': 'Climate change affects water resources through altered precipitation patterns, increased evaporation, and changing snow and ice patterns. Some regions experience more frequent droughts, while others face increased flooding. Mountain snowpack, which provides water for billions of people, is declining. Glaciers that serve as water towers for major rivers are shrinking. These changes threaten water security for drinking, agriculture, and hydroelectric power generation.',
                'category': 'impacts',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'How does climate change affect Arctic ice?',
                'answer': 'Climate change is dramatically affecting Arctic ice, with Arctic sea ice declining at a rate of about 13% per decade. The Arctic is warming twice as fast as the global average, a phenomenon called Arctic amplification. This ice loss reduces the Earth\'s ability to reflect sunlight, creating a feedback loop that accelerates warming. Melting Arctic ice contributes to sea level rise and disrupts global weather patterns and ocean currents.',
                'category': 'impacts',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What is coral bleaching?',
                'answer': 'Coral bleaching occurs when coral polyps expel the algae living in their tissues due to stress, primarily from rising ocean temperatures. The algae provide corals with food through photosynthesis, so when they\'re expelled, corals turn white (bleach) and can starve. While corals can recover if conditions improve, repeated or severe bleaching events can kill entire reef systems. Ocean acidification also weakens coral skeletons, making reefs more vulnerable.',
                'category': 'impacts',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
        ]
        
        # SOLUTIONS (25% of dataset)
        solutions = [
            {
                'question': 'What can individuals do to reduce their carbon footprint?',
                'answer': 'Individuals can reduce their carbon footprint through: 1) Energy conservation - using LED bulbs, improving home insulation, unplugging devices; 2) Transportation choices - walking, biking, public transit, or electric vehicles; 3) Diet changes - eating less meat, reducing food waste; 4) Consumption habits - buying less, choosing sustainable products, repairing instead of replacing; 5) Home energy - installing solar panels, using renewable energy; and 6) Advocacy - supporting climate policies and educating others.',
                'category': 'solutions',
                'difficulty': 'beginner',
                'source': 'manual_curation'
            },
            {
                'question': 'What are renewable energy sources?',
                'answer': 'Renewable energy sources are naturally replenishing resources that don\'t run out when used. The main types are: 1) Solar energy from sunlight; 2) Wind energy from moving air; 3) Hydroelectric power from flowing water; 4) Geothermal energy from Earth\'s heat; 5) Biomass from organic materials; and 6) Tidal energy from ocean movements. These sources produce little to no greenhouse gas emissions during operation, making them crucial for reducing climate change.',
                'category': 'solutions',
                'difficulty': 'beginner',
                'source': 'manual_curation'
            },
            {
                'question': 'What is carbon capture and storage?',
                'answer': 'Carbon capture and storage (CCS) is a technology that captures CO2 emissions from industrial sources before they enter the atmosphere and stores them underground or in other long-term storage. The process involves three steps: capturing CO2 from emissions sources, transporting it to storage sites, and injecting it into geological formations. CCS can help reduce emissions from power plants and industrial facilities while renewable energy scales up.',
                'category': 'solutions',
                'difficulty': 'advanced',
                'source': 'manual_curation'
            },
            {
                'question': 'How do forests help fight climate change?',
                'answer': 'Forests help fight climate change by acting as carbon sinks - they absorb CO2 from the atmosphere during photosynthesis and store it in trees and soil. A single mature tree can absorb 48 pounds of CO2 per year. Forests also provide cooling through evapotranspiration, regulate water cycles, and support biodiversity. Protecting existing forests and planting new ones are important climate solutions, but forest management must be sustainable to be effective.',
                'category': 'solutions',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What is the Paris Agreement?',
                'answer': 'The Paris Agreement is an international treaty adopted in 2015 where countries commit to limiting global warming to well below 2°C above pre-industrial levels, with efforts to limit it to 1.5°C. Each country sets its own climate targets (Nationally Determined Contributions) and reports on progress. The agreement includes provisions for climate finance to help developing countries. Nearly 200 countries have signed, making it the most comprehensive global climate agreement.',
                'category': 'solutions',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What is energy efficiency?',
                'answer': 'Energy efficiency means using less energy to provide the same level of service or output. Examples include LED light bulbs that use 75% less energy than incandescent bulbs, well-insulated buildings that require less heating and cooling, and efficient appliances that perform the same tasks with less electricity. Energy efficiency is often called the "first fuel" because the energy you don\'t use is the cleanest and cheapest energy of all.',
                'category': 'solutions',
                'difficulty': 'beginner',
                'source': 'manual_curation'
            },
            {
                'question': 'What are electric vehicles and how do they help climate?',
                'answer': 'Electric vehicles (EVs) use electric motors powered by batteries instead of internal combustion engines. They produce zero direct emissions and can significantly reduce transportation-related greenhouse gas emissions, especially when charged with renewable electricity. Even when accounting for electricity generation and battery production, EVs typically produce about half the lifetime emissions of conventional cars. As the electricity grid becomes cleaner, EVs become even more climate-friendly.',
                'category': 'solutions',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What is sustainable agriculture?',
                'answer': 'Sustainable agriculture uses farming practices that protect the environment, maintain soil health, and support farm communities while producing food efficiently. Key practices include crop rotation, cover crops, reduced tillage, integrated pest management, and precision farming. These methods can reduce greenhouse gas emissions, sequester carbon in soil, improve water quality, and maintain biodiversity while ensuring food security for a growing population.',
                'category': 'solutions',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What is net zero emissions?',
                'answer': 'Net zero emissions means achieving a balance between the greenhouse gases emitted and those removed from the atmosphere. This can be accomplished by reducing emissions as much as possible and offsetting remaining emissions through methods like carbon capture, reforestation, or other carbon removal technologies. Many countries and companies have committed to reaching net zero by 2050.',
                'category': 'solutions',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'How do solar panels work?',
                'answer': 'Solar panels work by converting sunlight into electricity using photovoltaic cells. When sunlight hits the silicon cells in the panel, it knocks electrons loose, creating an electric current. This direct current (DC) electricity is then converted to alternating current (AC) by an inverter, making it usable for homes and businesses. Solar panels produce clean electricity with no emissions during operation.',
                'category': 'solutions',
                'difficulty': 'beginner',
                'source': 'manual_curation'
            },
            {
                'question': 'What is climate adaptation?',
                'answer': 'Climate adaptation refers to adjustments in natural or human systems in response to actual or expected climate changes. Examples include building sea walls to protect against rising sea levels, developing drought-resistant crops, improving cooling systems for extreme heat, and updating building codes for severe weather. Adaptation complements mitigation efforts to reduce climate risks.',
                'category': 'solutions',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What are carbon offsets?',
                'answer': 'Carbon offsets are reductions in greenhouse gas emissions made to compensate for emissions produced elsewhere. Examples include planting trees, investing in renewable energy projects, or supporting methane capture from landfills. One carbon offset represents one metric ton of CO2 equivalent removed or prevented. While useful, offsets should supplement, not replace, direct emission reductions.',
                'category': 'solutions',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
        ]
        
        # DATA AND TRENDS (10% of dataset)
        data_trends = [
            {
                'question': 'How much has global temperature increased?',
                'answer': 'Global average temperature has increased by approximately 1.1°C (2°F) since the late 1800s. The warming has accelerated in recent decades, with the last decade being the warmest on record. Each of the last four decades has been successively warmer than any decade before it since 1850. The year 2023 was the warmest year on record globally, and 19 of the 20 warmest years have occurred since 2000.',
                'category': 'data_trends',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'How much have carbon dioxide levels increased?',
                'answer': 'Atmospheric CO2 levels have increased from about 280 parts per million (ppm) before the Industrial Revolution to over 420 ppm today - an increase of more than 40%. This is the highest level in over 3 million years. The rate of increase has accelerated, with CO2 levels rising by about 2.5 ppm per year in recent decades. Ice core data shows this increase is unprecedented in human history.',
                'category': 'data_trends',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What do climate models predict for the future?',
                'answer': 'Climate models predict that without significant action, global temperatures could rise 3-5°C by 2100. Even with current commitments, warming is likely to exceed 2°C. Models project more frequent extreme weather, continued sea level rise, shifts in precipitation patterns, and ecosystem changes. However, rapid decarbonization could limit warming to 1.5-2°C. Models have been accurate in predicting past climate changes, giving confidence in future projections.',
                'category': 'data_trends',
                'difficulty': 'advanced',
                'source': 'manual_curation'
            },
            {
                'question': 'How fast is sea level rising?',
                'answer': 'Global sea level is currently rising at about 3.3 millimeters per year, which is more than twice the rate observed in the 20th century. Since 1993, satellite measurements show sea levels have risen by about 10 centimeters (4 inches). The rate is accelerating due to increased ice melting from Greenland and Antarctica, plus thermal expansion of warming oceans. Without action, sea levels could rise 0.5-2 meters by 2100.',
                'category': 'data_trends',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
            {
                'question': 'What percentage of scientists agree on climate change?',
                'answer': 'Multiple studies show that 97-99% of actively publishing climate scientists agree that climate change is happening and is primarily caused by human activities. This consensus is based on analysis of thousands of peer-reviewed papers and surveys of climate experts. The scientific consensus on human-caused climate change is as strong as the consensus on other well-established scientific facts, such as the link between smoking and cancer.',
                'category': 'data_trends',
                'difficulty': 'intermediate',
                'source': 'manual_curation'
            },
        ]
        
        # Add some IPCC-based content for credibility
        ipcc_content = [
            {
                'question': 'What is the current state of global warming according to the latest IPCC report?',
                'answer': 'According to the IPCC AR6 report, global surface temperature has increased by approximately 1.1°C since 1850-1900. This warming is unequivocally caused by human activities, primarily greenhouse gas emissions from burning fossil fuels. The warming has occurred across all regions and seasons, with the most recent decade being the warmest on record.',
                'category': 'data_trends',
                'difficulty': 'advanced',
                'source': 'ipcc_ar6'
            },
            {
                'question': 'What are the main human activities contributing to climate change?',
                'answer': 'The primary human activities contributing to climate change include: burning fossil fuels (coal, oil, gas) for electricity, heat, and transportation; deforestation and land use changes; industrial processes; and agriculture. Fossil fuel burning is the largest source, accounting for about 75% of global greenhouse gas emissions.',
                'category': 'basic_concepts',
                'difficulty': 'beginner',
                'source': 'ipcc_ar6'
            },
            {
                'question': 'What are the projected impacts of climate change?',
                'answer': 'Climate change impacts include rising sea levels, more frequent extreme weather events, changes in precipitation patterns, ecosystem disruption, and threats to food and water security. The severity depends on future emissions, but some impacts are already locked in due to past emissions. Without significant action, global temperatures could rise 3-5°C by 2100.',
                'category': 'impacts',
                'difficulty': 'intermediate',
                'source': 'ipcc_ar6'
            },
            {
                'question': 'What solutions exist to address climate change?',
                'answer': 'Climate solutions include transitioning to renewable energy, improving energy efficiency, protecting and restoring forests, developing carbon capture technologies, and changing consumption patterns. Rapid, far-reaching transitions in energy, land, urban infrastructure, and industrial systems are needed to limit warming to 1.5°C.',
                'category': 'solutions',
                'difficulty': 'intermediate',
                'source': 'ipcc_ar6'
            },
        ]
        
        # Combine all categories
        dataset.extend(basic_concepts)
        dataset.extend(impacts)
        dataset.extend(solutions)
        dataset.extend(data_trends)
        dataset.extend(ipcc_content)
        
        return dataset
    
    def create_question_variations(self, base_dataset: List[Dict]) -> List[Dict]:
        """
        Create question variations to expand the dataset
        """
        variations = []
        
        # Question starters and their alternatives
        variation_patterns = {
            "What is": ["Can you explain", "How would you define", "Tell me about"],
            "How does": ["In what way does", "What is the mechanism of", "By what process does"],
            "Why does": ["What causes", "What is the reason", "How come"],
            "What are": ["Can you list", "What would be examples of", "Name some"],
            "How do": ["What is the process by which", "In what way do", "By what means do"]
        }
        
        for entry in base_dataset:
            original_question = entry['question']
            
            # Try to create one variation per original question
            for original_start, alternatives in variation_patterns.items():
                if original_question.startswith(original_start):
                    # Use the first alternative
                    new_start = alternatives[0]
                    new_question = original_question.replace(original_start, new_start, 1)
                    
                    # Create new entry
                    new_entry = entry.copy()
                    new_entry['question'] = new_question
                    new_entry['source'] = f"{entry['source']}_variation"
                    
                    variations.append(new_entry)
                    break
        
        return variations
    
    def add_education_specific_content(self) -> List[Dict]:
        """
        Add content specific to climate education scenarios
        """
        education_content = [
            {
                'question': 'How can teachers explain climate change to young students?',
                'answer': 'Teachers can explain climate change to young students using simple analogies, hands-on experiments, and relatable examples. Compare the greenhouse effect to a blanket keeping Earth warm, use a thermometer to show temperature changes, and relate impacts to local weather patterns. Visual aids like charts, videos, and interactive games help make abstract concepts concrete. Focus on solutions and positive actions students can take to feel empowered rather than overwhelmed.',
                'category': 'solutions',
                'difficulty': 'intermediate',
                'source': 'education_specific'
            },
            {
                'question': 'What are some simple climate change experiments for students?',
                'answer': 'Simple experiments include: 1) Greenhouse effect demonstration using glass jars and thermometers to show temperature differences; 2) Ice melting experiments to show thermal expansion; 3) Ocean acidification using pH strips and carbonated water; 4) Carbon cycle modeling with role-playing activities; 5) Solar oven building to demonstrate renewable energy; and 6) Tree ring analysis to understand climate history. These hands-on activities make climate science tangible and engaging.',
                'category': 'basic_concepts',
                'difficulty': 'beginner',
                'source': 'education_specific'
            },
            {
                'question': 'How do we teach climate solutions without causing eco-anxiety?',
                'answer': 'Focus on positive, actionable solutions rather than just problems. Emphasize that many smart people are working on climate solutions and significant progress is being made. Share success stories of renewable energy growth, conservation efforts, and youth climate activists. Encourage students to take age-appropriate actions like energy conservation, recycling, and learning about sustainability. Frame climate action as an opportunity for innovation and positive change.',
                'category': 'solutions',
                'difficulty': 'intermediate',
                'source': 'education_specific'
            },
            {
                'question': 'What age-appropriate climate actions can students take?',
                'answer': 'Students can take many climate actions: turning off lights and electronics when not in use, walking or biking instead of driving short distances, recycling and reducing waste, eating less meat occasionally, learning about renewable energy, participating in tree planting, starting a school environmental club, and talking to family about climate-friendly choices. The key is making actions feel empowering rather than overwhelming.',
                'category': 'solutions',
                'difficulty': 'beginner',
                'source': 'education_specific'
            },
            {
                'question': 'How can students learn about local climate impacts?',
                'answer': 'Students can study local climate impacts by monitoring local weather patterns, researching historical climate data for their region, interviewing older community members about weather changes they\'ve observed, studying local ecosystem changes, examining how local agriculture is adapting, and investigating what their city or region is doing to address climate change. This makes global climate change personally relevant and tangible.',
                'category': 'impacts',
                'difficulty': 'intermediate',
                'source': 'education_specific'
            },
        ]
        
        return education_content
    
    def build_complete_dataset(self) -> List[Dict]:
        """
        Build the complete dataset with all components
        """
        print("Building comprehensive climate education dataset...")
        
        # Create base dataset
        base_dataset = self.create_base_dataset()
        print(f"Created {len(base_dataset)} base Q&A pairs")
        
        # Add education-specific content
        education_content = self.add_education_specific_content()
        base_dataset.extend(education_content)
        print(f"Added {len(education_content)} education-specific pairs")
        
        # Create question variations
        variations = self.create_question_variations(base_dataset)
        all_dataset = base_dataset + variations
        print(f"Created {len(variations)} question variations")
        
        # Add metadata to all entries
        for i, entry in enumerate(all_dataset):
            entry['id'] = f"climate_qa_{i+1:03d}"
            entry['word_count'] = len(entry['answer'].split())
            entry['char_count'] = len(entry['answer'])
            entry['created_date'] = '2024-12-01'
            entry['url'] = entry.get('url', 'manual_creation')
        
        print(f"Total dataset size: {len(all_dataset)} Q&A pairs")
        return all_dataset
    
    def save_dataset(self, dataset: List[Dict], filename: str = "climate_dataset"):
        """
        Save the dataset with comprehensive statistics
        """
        # Save as JSON
        json_filename = f"{filename}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        
        # Save as CSV
        csv_filename = f"{filename}.csv"
        df = pd.DataFrame(dataset)
        df.to_csv(csv_filename, index=False)
        
        # Print comprehensive statistics
        self.print_dataset_statistics(df, json_filename, csv_filename)
        
        return df
    
    def print_dataset_statistics(self, df: pd.DataFrame, json_file: str, csv_file: str):
        """
        Print comprehensive dataset statistics
        """
        print(f"\n{'='*70}")
        print(f"CLIMATE EDUCATION DATASET - READY FOR TRAINING!")
        print(f"{'='*70}")
        
        print(f"DATASET OVERVIEW:")
        print(f"   Total Q&A pairs: {len(df)}")
        print(f"   Files created: {json_file}, {csv_file}")
        
        print(f"\nCATEGORY DISTRIBUTION:")
        category_stats = df['category'].value_counts()
        for category, count in category_stats.items():
            percentage = (count / len(df)) * 100
            print(f"   {category.replace('_', ' ').title()}: {count} pairs ({percentage:.1f}%)")
        
        print(f"\nDIFFICULTY DISTRIBUTION:")
        difficulty_stats = df['difficulty'].value_counts()
        for difficulty, count in difficulty_stats.items():
            percentage = (count / len(df)) * 100
            print(f"   {difficulty.title()}: {count} pairs ({percentage:.1f}%)")
        
        print(f"\nSOURCE DISTRIBUTION:")
        source_stats = df['source'].value_counts()
        for source, count in source_stats.items():
            print(f"   {source}: {count} pairs")
        
        print(f"\nCONTENT QUALITY METRICS:")
        print(f"   Average answer length: {df['word_count'].mean():.1f} words")
        print(f"   Shortest answer: {df['word_count'].min()} words")
        print(f"   Longest answer: {df['word_count'].max()} words")
        print(f"   Median answer length: {df['word_count'].median():.1f} words")
        print(f"   Total characters: {df['char_count'].sum():,}")
        
        print(f"\nTRAINING READINESS ASSESSMENT:")
        if len(df) >= 200:
            print(f"   Dataset Size: EXCELLENT ({len(df)} pairs)")
            print(f"   Recommendation: Perfect for robust transformer training")
        elif len(df) >= 100:
            print(f"   Dataset Size: GOOD ({len(df)} pairs)")
            print(f"   Recommendation: Sufficient for effective training")
        elif len(df) >= 50:
            print(f"   Dataset Size: ACCEPTABLE ({len(df)} pairs)")
            print(f"   Recommendation: Minimal but workable for assignment")
        else:
            print(f"   Dataset Size: TOO SMALL ({len(df)} pairs)")
            print(f"   Recommendation: Need more data for effective training")
        
        print(f"\nSAMPLE ENTRIES:")
        # Show samples from each category
        categories = df['category'].unique()
        for i, category in enumerate(categories[:3]):  # Show first 3 categories
            sample = df[df['category'] == category].iloc[0]
            print(f"\n   {i+1}. {category.replace('_', ' ').title()} Example:")
            print(f"      Q: {sample['question']}")
            print(f"      A: {sample['answer'][:120]}...")
            print(f"      Difficulty: {sample['difficulty']}, Words: {sample['word_count']}")
        
        print(f"\n{'='*70}")
        print(f"DATASET CREATION COMPLETE! Ready for transformer training!")
        print(f"{'='*70}")

# Main execution function
def main():
    """
    Main function to create the complete climate education dataset
    """
    # Check if dataset already exists
    if os.path.exists("climate_dataset.csv"):
        print("Dataset already exists! Do you want to:")
        print("1. Use existing dataset")
        print("2. Create new dataset (will overwrite)")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == "1":
            print("Loading existing dataset...")
            df = pd.read_csv("climate_dataset.csv")
            print(f"Loaded {len(df)} Q&A pairs from existing dataset.")
            return df
        elif choice != "2":
            print("Invalid choice. Exiting.")
            return None
    
    # Create new dataset
    builder = ClimateDatasetBuilder()
    
    try:
        # Build the dataset
        dataset = builder.build_complete_dataset()
        
        # Save the dataset
        df = builder.save_dataset(dataset)
        
        # Create train/test split files for convenience
        from sklearn.model_selection import train_test_split
        
        train_data, temp_data = train_test_split(dataset, test_size=0.3, random_state=42)
        val_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42)
        
        # Save split datasets
        pd.DataFrame(train_data).to_csv("climate_train_data.csv", index=False)
        pd.DataFrame(val_data).to_csv("climate_val_data.csv", index=False)
        pd.DataFrame(test_data).to_csv("climate_test_data.csv", index=False)
        
        print(f"\nTRAIN/VALIDATION/TEST SPLIT CREATED:")
        print(f"   Training data: {len(train_data)} pairs (climate_train_data.csv)")
        print(f"   Validation data: {len(val_data)} pairs (climate_val_data.csv)")
        print(f"   Test data: {len(test_data)} pairs (climate_test_data.csv)")
        
        return df
        
    except Exception as e:
        print(f"Error creating dataset: {e}")
        logger.error(f"Dataset creation failed: {e}")
        return None

# Entry point
if __name__ == "__main__":
    print("Starting Climate Education Dataset Builder...")
    print("This will create a comprehensive dataset for the transformer chatbot; AyikaBot.")
    
    # Create the dataset
    result_df = main()
    
    if result_df is not None:
        print(f"\nSUCCESS! The climate education dataset is ready!")
        print(f"Files created in current directory:")
        print(f"   - climate_dataset.csv (main dataset)")
        print(f"   - climate_dataset.json (JSON format)")
        print(f"   - climate_train_data.csv (training split)")
        print(f"   - climate_val_data.csv (validation split)")
        print(f"   - climate_test_data.csv (test split)")
    else:
        print("Dataset creation failed. Please check the error messages above.")
