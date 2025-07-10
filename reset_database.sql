-- Quick Database Reset Script for Testing
-- Run this in your Supabase SQL editor to reset the database for testing

-- Drop existing policies
DROP POLICY IF EXISTS "Users can view all profiles" ON public.profiles;
DROP POLICY IF EXISTS "Users can insert their own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can update their own profile" ON public.profiles;
DROP POLICY IF EXISTS "Service role can insert profiles" ON public.profiles;
DROP POLICY IF EXISTS "Anyone can view profiles" ON public.profiles;
DROP POLICY IF EXISTS "Anyone can insert profiles" ON public.profiles;


DROP POLICY IF EXISTS "Anyone can view answered questions" ON public.questions;
DROP POLICY IF EXISTS "Users can view their own questions" ON public.questions;
DROP POLICY IF EXISTS "Anyone can insert questions" ON public.questions;
DROP POLICY IF EXISTS "Users can update their own questions" ON public.questions;
DROP POLICY IF EXISTS "Users can delete their own questions" ON public.questions;

-- Clear test data
DELETE FROM public.questions WHERE receiver = 'testuser';
DELETE FROM public.profiles WHERE username = 'testuser';

-- Recreate policies with more permissive rules for testing
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
        ) OR auth.uid() IS NULL
    );

CREATE POLICY "Anyone can insert questions" ON public.questions
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update their own questions" ON public.questions
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE profiles.username = questions.receiver 
            AND profiles.id = auth.uid()
        ) OR auth.uid() IS NULL
    );

CREATE POLICY "Users can delete their own questions" ON public.questions
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE profiles.username = questions.receiver 
            AND profiles.id = auth.uid()
        ) OR auth.uid() IS NULL
    );
