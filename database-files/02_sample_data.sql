-- Insert sample learning style distribution data
INSERT INTO learning_style_distribution (userid, visual_percentage, auditory_percentage, reading_writing_percentage, kinesthetic_percentage)
VALUES 
(1, 65.00, 15.00, 10.00, 10.00),
(2, 25.00, 40.00, 20.00, 15.00),
(3, 30.00, 20.00, 35.00, 15.00),
(4, 20.00, 25.00, 25.00, 30.00),
(5, 40.00, 20.00, 25.00, 15.00);

-- Insert sample learning style profile data
INSERT INTO learning_style_profile (userid, strengths, areas_for_growth)
VALUES 
(1, 'Visual memory, Pattern recognition, Spatial awareness', 'Auditory learning, Note-taking speed'),
(2, 'Active listening, Group discussions, Verbal explanations', 'Visual organization, Written summaries'),
(3, 'Note organization, Written expression, Reading comprehension', 'Hands-on activities, Visual diagrams'),
(4, 'Physical activities, Hands-on experiments, Movement-based learning', 'Abstract concepts, Traditional lectures'),
(5, 'Diagram interpretation, Visual planning, Mind mapping', 'Verbal presentations, Group discussions');

-- Insert sample study techniques
INSERT INTO study_techniques (learning_style, technique_description)
VALUES 
('visual', 'Use mind maps and diagrams to visualize concepts'),
('visual', 'Create color-coded notes and highlights'),
('visual', 'Draw flowcharts for processes and relationships'),
('auditory', 'Record and listen to lecture summaries'),
('auditory', 'Participate in group discussions'),
('auditory', 'Explain concepts out loud to yourself or others'),
('reading_writing', 'Create detailed written summaries'),
('reading_writing', 'Rewrite notes in your own words'),
('reading_writing', 'Practice writing explanations of concepts'),
('kinesthetic', 'Use physical objects to model concepts'),
('kinesthetic', 'Take breaks for movement between study sessions'),
('kinesthetic', 'Create hands-on experiments or demonstrations');

-- Insert sample study tools
INSERT INTO study_tools (learning_style, tool_name, tool_description)
VALUES 
('visual', 'Mind Mapping Software', 'Tools like MindMeister or XMind for visual organization'),
('visual', 'Digital Whiteboard', 'Online whiteboard for drawing and diagramming'),
('auditory', 'Voice Recorder', 'Record and playback study materials'),
('auditory', 'Text-to-Speech', 'Convert written materials to audio'),
('reading_writing', 'Note-Taking App', 'Digital tools for organized note-taking'),
('reading_writing', 'Flashcard App', 'Create and review digital flashcards'),
('kinesthetic', 'Educational Models', 'Physical models for hands-on learning'),
('kinesthetic', 'Interactive Simulations', 'Virtual labs and interactive exercises');

-- Insert sample study group recommendations
INSERT INTO study_group_recommendations (learning_style, recommendation_description)
VALUES 
('visual', 'Join groups that use visual aids and diagrams in study sessions'),
('visual', 'Form groups for creating mind maps and visual summaries'),
('auditory', 'Participate in discussion-based study groups'),
('auditory', 'Join groups that focus on verbal explanations and debates'),
('reading_writing', 'Form groups for sharing written notes and summaries'),
('reading_writing', 'Join groups focused on creating study guides'),
('kinesthetic', 'Join groups that incorporate hands-on activities'),
('kinesthetic', 'Form groups for practical experiments and demonstrations');

-- Insert learning style distribution for existing users
INSERT INTO learning_style_distribution (userid, visual_percentage, auditory_percentage, reading_writing_percentage, kinesthetic_percentage)
SELECT 
    userid,
    CASE 
        WHEN learning_style = 'visual' THEN 65.00
        WHEN learning_style = 'auditory' THEN 25.00
        WHEN learning_style = 'kinesthetic' THEN 30.00
    END as visual_percentage,
    CASE 
        WHEN learning_style = 'visual' THEN 15.00
        WHEN learning_style = 'auditory' THEN 40.00
        WHEN learning_style = 'kinesthetic' THEN 20.00
    END as auditory_percentage,
    CASE 
        WHEN learning_style = 'visual' THEN 10.00
        WHEN learning_style = 'auditory' THEN 20.00
        WHEN learning_style = 'kinesthetic' THEN 35.00
    END as reading_writing_percentage,
    CASE 
        WHEN learning_style = 'visual' THEN 10.00
        WHEN learning_style = 'auditory' THEN 15.00
        WHEN learning_style = 'kinesthetic' THEN 15.00
    END as kinesthetic_percentage
FROM user;

-- Insert learning style profiles for existing users
INSERT INTO learning_style_profile (userid, strengths, areas_for_growth)
SELECT 
    userid,
    CASE 
        WHEN learning_style = 'visual' THEN 'Visual memory, Pattern recognition, Spatial awareness'
        WHEN learning_style = 'auditory' THEN 'Active listening, Group discussions, Verbal explanations'
        WHEN learning_style = 'kinesthetic' THEN 'Physical activities, Hands-on experiments, Movement-based learning'
    END as strengths,
    CASE 
        WHEN learning_style = 'visual' THEN 'Auditory learning, Note-taking speed'
        WHEN learning_style = 'auditory' THEN 'Visual organization, Written summaries'
        WHEN learning_style = 'kinesthetic' THEN 'Abstract concepts, Traditional lectures'
    END as areas_for_growth
FROM user;

-- Insert study techniques for each learning style
INSERT INTO study_techniques (learning_style, technique_description)
VALUES 
('visual', 'Use mind maps and diagrams to visualize concepts'),
('visual', 'Create color-coded notes and highlights'),
('visual', 'Draw flowcharts for processes and relationships'),
('auditory', 'Record and listen to lecture summaries'),
('auditory', 'Participate in group discussions'),
('auditory', 'Explain concepts out loud to yourself or others'),
('kinesthetic', 'Use physical objects to model concepts'),
('kinesthetic', 'Take breaks for movement between study sessions'),
('kinesthetic', 'Create hands-on experiments or demonstrations');

-- Insert study tools for each learning style
INSERT INTO study_tools (learning_style, tool_name, tool_description)
VALUES 
('visual', 'Mind Mapping Software', 'Tools like MindMeister or XMind for visual organization'),
('visual', 'Digital Whiteboard', 'Online whiteboard for drawing and diagramming'),
('auditory', 'Voice Recorder', 'Record and playback study materials'),
('auditory', 'Text-to-Speech', 'Convert written materials to audio'),
('kinesthetic', 'Educational Models', 'Physical models for hands-on learning'),
('kinesthetic', 'Interactive Simulations', 'Virtual labs and interactive exercises');

-- Insert study group recommendations for each learning style
INSERT INTO study_group_recommendations (learning_style, recommendation_description)
VALUES 
('visual', 'Join groups that use visual aids and diagrams in study sessions'),
('visual', 'Form groups for creating mind maps and visual summaries'),
('auditory', 'Participate in discussion-based study groups'),
('auditory', 'Join groups that focus on verbal explanations and debates'),
('kinesthetic', 'Join groups that incorporate hands-on activities'),
('kinesthetic', 'Form groups for practical experiments and demonstrations'); 