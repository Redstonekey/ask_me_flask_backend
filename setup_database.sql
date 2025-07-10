-- AskMe Database Setup Script
-- Run this in your Supabase SQL editor

-- Create profiles table (extends auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (id)
);

-- Create questions table (already exists based on your schema)
CREATE TABLE IF NOT EXISTS public.questions (
    id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    sender TEXT,
    receiver TEXT NOT NULL,
    answered BOOLEAN DEFAULT FALSE,
    question TEXT NOT NULL,
    answer TEXT,
    answered_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT questions_pkey PRIMARY KEY (id)
);

-- Add foreign key constraint to link questions to profiles
ALTER TABLE public.questions 
ADD CONSTRAINT fk_receiver 
FOREIGN KEY (receiver) REFERENCES public.profiles(username) ON DELETE CASCADE;

-- Enable Row Level Security (RLS) - but allow anon access for profiles
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.questions ENABLE ROW LEVEL SECURITY;

-- RLS Policies for profiles table
CREATE POLICY "Anyone can view profiles" ON public.profiles
    FOR SELECT USING (true);

CREATE POLICY "Anyone can insert profiles" ON public.profiles
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update their own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = id OR auth.uid() IS NULL);

-- RLS Policies for questions table
CREATE POLICY "Anyone can view answered questions" ON public.questions
    FOR SELECT USING (answered = true);

CREATE POLICY "Users can view their own questions" ON public.questions
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE profiles.username = questions.receiver 
            AND profiles.id = auth.uid()
        )
    );

CREATE POLICY "Anyone can insert questions" ON public.questions
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update their own questions" ON public.questions
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE profiles.username = questions.receiver 
            AND profiles.id = auth.uid()
        )
    );

CREATE POLICY "Users can delete their own questions" ON public.questions
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE profiles.username = questions.receiver 
            AND profiles.id = auth.uid()
        )
    );

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_questions_receiver ON public.questions(receiver);
CREATE INDEX IF NOT EXISTS idx_questions_answered ON public.questions(answered);
CREATE INDEX IF NOT EXISTS idx_questions_created_at ON public.questions(created_at);
CREATE INDEX IF NOT EXISTS idx_profiles_username ON public.profiles(username);

-- Create a function to handle user profile creation
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    -- This function will be called when a new user signs up
    -- You can customize this to automatically create a profile
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for new user signup (optional)
-- CREATE TRIGGER on_auth_user_created
--     AFTER INSERT ON auth.users
--     FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Grant necessary permissions
GRANT ALL ON public.profiles TO authenticated;
GRANT ALL ON public.questions TO authenticated;
GRANT ALL ON public.profiles TO anon;
GRANT ALL ON public.questions TO anon;
