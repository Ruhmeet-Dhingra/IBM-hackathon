from brain.entity_extractor import EntityExtractor

extractor = EntityExtractor()

entities = extractor.extract("Open Chrome")

for entity in entities:
    print(entity)
    print(entity.type)
    print(entity.name)