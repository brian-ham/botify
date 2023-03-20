from sentence_transformers import SentenceTransformer, util
import numpy as np
import pandas as pd

# Model Selection
model = SentenceTransformer('stsb-roberta-large') # most up-to-date model

# Adapted from Christian Schubart's "Ideen zu einer Aesthetik der Tonkunst" (1806)
key_desc = ["Completely pure. Simplicity and naivety. The key of children. Free of burden, full of imagination. Powerful resolve. Earnestness. Can feel religious.",
"Declarations of love and lamenting lost love or unhappy relationships. It is languishing and full of longing, a soul in search of something different.",
"Rapture in sadness. A grimacing key of choking back tears. It is capable of a laugh or smile to pacify those around, but the truth is in despair. Fullness of tone, sonority, and euphony.",
"A passionate expression of sorrow and deep grief. Full of penance and self-punishment. An intimate conversation with God about recognition of wrongdoing and atonement.",
"Screaming hallelujah's, rejoicing in conquering obstacles. War marches, holiday songs, invitations to join the winning team.",
"Melancholy, feminine, brooding worries, contemplation of negativity.",
"Love, Devotion, Intimacy, Openness, Honest Communion. Conversations with God.",
"Dealing with anxiety and existential terror, deep distress, dark depression. The dark night of the soul. Fear, hesitation, shuddering, goose bumps. The language of ghosts.",
"Shouts of Joy, Complete Delight, yet Bickering, Short-fused, Ready to Fight.",
"This key can carry grief, mournfulness, restlessness. Like a princess locked in a tower longing for her rescuer and future lover.",
"Complaisance, Controlled calmness over the readiness to explode. Deeply angry but composed and sociable still. Religious sentiment.",
"Deepest depression, lament over death and loss, groans of misery, ready to expire. Harrowing. Melancholic.",
"Triumph over evil, obstacles, hurdles. Surmounting foes and finally finding rest in victory. Brilliant clarity of thought and feeling.",
"Tearing at your hair and shirt, discontentment, long periods of lamentation and crying. Still capable of fighting this feeling.",
"Rustic, Idyllic, Poetic, Lyrical. Calm and satisfied. Tenderness and Gratitude. Friendship and Faith. It is a gentle key full of peace.",
"Worry of the future, of a failed plan, gnashing of teeth. Concern over a failed plan. Struggling with dislike and malcontent.",
"Putrefaction, Expansive viewpoints of a dark cosmos and existence. Ghosts, Ghouls, Goblins, Graveyards. Haunting and Lingering.",
"Suffocation of the Heart, Lamentations, Life-Long Struggles. A negative look at the experiences of life, competition, growth.",
"Innocent Love, Satisfaction with the current state of affairs. Optimistic. Belief in Heaven and reuniting with lost loved ones. Youthful and cheerful. Trusting in the spirit of the divine.",
"Womanly, Graceful in character. Capable of soothing.",
"Love, Clear Conscience, Hopeful Aspirations for the future and a better world. Optimistic and able to take control in order to ensure peace.",
"The Garment of Night, Surly, Blasphemous, Turning away the world and the divine. Preparations for the end. Pessimism and giving up. Belief in darkness.",
"Uncontrolled passions. Angry, Jealous, Fury, Despair, Burdened with negative energy. Prepared to fight.",
"The key of patience, calmly waiting for fate, destiny, and the submission to providence and karma."
]

# Compute embeddings: NumPy array of shape (24, 1024)
embeddings = model.encode(key_desc)
print(embeddings.transpose().shape)
df = pd.DataFrame(embeddings.transpose(), columns=[i for i in range(24)])
df.to_csv("key_embeddings.csv", index=False)

# should have contingency for when there is very little simliarity (ex. inputted gibberish)