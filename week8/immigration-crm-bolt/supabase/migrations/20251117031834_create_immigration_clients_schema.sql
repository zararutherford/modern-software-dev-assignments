/*
  # Immigration Client CRM Database Schema

  1. New Tables
    - `clients`
      - `id` (uuid, primary key) - Unique client identifier
      - `user_id` (uuid, foreign key) - Attorney who owns this client record
      - `first_name` (text) - Client's first name
      - `last_name` (text) - Client's last name
      - `email` (text) - Client's email address
      - `phone` (text) - Client's phone number
      - `date_of_birth` (date) - Client's date of birth
      - `country_of_origin` (text) - Client's country of origin
      - `visa_type` (text) - Type of visa/immigration status
      - `case_status` (text) - Current status of their case
      - `priority` (text) - Case priority level
      - `filing_date` (date) - Date case was filed
      - `notes` (text) - Additional notes about the client
      - `created_at` (timestamptz) - Record creation timestamp
      - `updated_at` (timestamptz) - Record last update timestamp

  2. Security
    - Enable RLS on `clients` table
    - Add policies for authenticated attorneys to manage their own clients:
      - Attorneys can view their own clients
      - Attorneys can insert new clients
      - Attorneys can update their own clients
      - Attorneys can delete their own clients

  3. Important Notes
    - All client data is private and can only be accessed by the attorney who created it
    - Case statuses include: pending, in_review, approved, denied, closed
    - Priority levels: low, medium, high, urgent
    - Visa types commonly include: H1B, L1, Green Card, Citizenship, etc.
*/

CREATE TABLE IF NOT EXISTS clients (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  first_name text NOT NULL,
  last_name text NOT NULL,
  email text,
  phone text,
  date_of_birth date,
  country_of_origin text NOT NULL,
  visa_type text NOT NULL,
  case_status text NOT NULL DEFAULT 'pending',
  priority text NOT NULL DEFAULT 'medium',
  filing_date date,
  notes text DEFAULT '',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE clients ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Attorneys can view own clients"
  ON clients FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Attorneys can insert own clients"
  ON clients FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Attorneys can update own clients"
  ON clients FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Attorneys can delete own clients"
  ON clients FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

CREATE INDEX IF NOT EXISTS idx_clients_user_id ON clients(user_id);
CREATE INDEX IF NOT EXISTS idx_clients_case_status ON clients(case_status);
CREATE INDEX IF NOT EXISTS idx_clients_priority ON clients(priority);