from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.models import Topic as TopicOrm


async def seed_topics(db: AsyncSession):
    topics = [
        {
            "content": "Artificial Intelligence (AI) is revolutionizing various sectors by enabling machines to perform tasks that typically require human intelligence. This encompasses a range of activities such as learning, reasoning, problem-solving, and understanding natural language. AI technologies, like machine learning and deep learning, utilize vast amounts of data to recognize patterns, make decisions, and predict outcomes with increasing accuracy. From personalized recommendations on streaming services to advanced medical diagnostics, AI is enhancing efficiency and innovation across industries. However, this rapid advancement also raises ethical considerations, including concerns about job displacement, data privacy, and the potential for biased decision-making. As AI continues to evolve, it holds the promise of transformative benefits while necessitating thoughtful regulation and responsible use.",
            "description": "AI",
            "generation_type": "SEEDED",
            "tags": ["AI", "Tech"],
            "title": "Artificial Intelligence",
        },
        {
            "content": "The economy of India, one of the world's fastest-growing major economies, is characterized by a blend of traditional agriculture, modern industries, and a burgeoning services sector. As the fifth-largest economy globally by nominal GDP, India has made significant strides in economic development, driven by liberalization policies and a vibrant private sector. Key industries include information technology, telecommunications, textiles, chemicals, pharmaceuticals, biotechnology, and steel production. Agriculture, although its share in GDP has declined, remains a vital sector, providing employment to a significant portion of the population. India's economic growth is further bolstered by a large and youthful workforce, urbanization, and increasing foreign investments. However, the country faces challenges such as income inequality, unemployment, infrastructure deficits, and regulatory hurdles. Addressing these issues is crucial for sustaining long-term growth and ensuring that the benefits of economic progress are widely distributed across its diverse population.",
            "description": "",
            "generation_type": "SEEDED",
            "tags": ["Economics", "Country"],
            "title": "Indian Economy",
        },
        {
            "content": "Climate change represents one of the most pressing global challenges of our time, driven primarily by human activities such as burning fossil fuels, deforestation, and industrial processes. These activities increase the concentration of greenhouse gases in the atmosphere, leading to global warming and altering weather patterns. The impacts of climate change are widespread and profound, including rising sea levels, more frequent and severe extreme weather events, loss of biodiversity, and disruptions to agricultural productivity. Mitigating climate change requires a coordinated effort to reduce carbon emissions, transition to renewable energy sources, and adopt sustainable practices across all sectors of society. Additionally, adaptation strategies are essential to cope with the inevitable changes that are already underway, ensuring resilience and protection for vulnerable communities and ecosystems.",
            "description": "",
            "generation_type": "SEEDED",
            "tags": ["Climate", "Earth", "Environment"],
            "title": "Climate Change",
        },
        {
            "content": "Quantum computing is an emerging field that leverages the principles of quantum mechanics to perform computations far more efficiently than classical computers. Unlike classical bits, which represent data as either 0 or 1, quantum bits or qubits can exist in multiple states simultaneously thanks to superposition. This property, along with entanglement and quantum tunneling, allows quantum computers to solve certain complex problems much faster than their classical counterparts. Potential applications of quantum computing include cryptography, drug discovery, optimization problems, and climate modeling. While still in the experimental stages, significant advancements are being made, with companies and research institutions racing to develop practical and scalable quantum systems. The full realization of quantum computing promises to revolutionize technology and various scientific fields, although it also poses challenges, such as ensuring security and managing quantum coherence.",
            "description": "",
            "generation_type": "SEEDED",
            "tags": ["Computers", "Quantum Computing", "Tech"],
            "title": "Quantum Computing",
        },
        {
            "content": "Space exploration has captivated human imagination and ambition, leading to remarkable achievements and profound scientific discoveries. From the historic Apollo moon landings to the ongoing missions to Mars, space exploration expands our understanding of the universe and our place within it. Modern missions, such as those by NASA, ESA, SpaceX, and other international and private entities, focus on various objectives including studying planetary bodies, searching for extraterrestrial life, and developing technologies for long-term human habitation in space. Advances in robotics, propulsion, and materials science are driving these endeavors, making space more accessible than ever before. Additionally, space exploration spurs innovation, inspires new generations of scientists and engineers, and fosters international collaboration. The potential for mining asteroids, utilizing space resources, and establishing human colonies on other planets opens new frontiers for economic growth and human survival. However, it also necessitates careful consideration of ethical, legal, and environmental issues to ensure the responsible use of outer space.",
            "description": "",
            "generation_type": "SEEDED",
            "tags": ["Space", "Science"],
            "title": "Space Exploration",
        },
    ]

    for topic in topics:
        item = TopicOrm(**topic)
        db.add(item)
