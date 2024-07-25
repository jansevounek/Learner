import { createClient } from "@supabase/supabase-js";

const supabaseUrl = 'https://ujelpwjscjrsaqgocyae.supabase.co';
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVqZWxwd2pzY2pyc2FxZ29jeWFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE1ODg1OTAsImV4cCI6MjAzNzE2NDU5MH0.4mjGriqAFZEDQmP-LejpeiEV6eOqUOWMNYLPkDgy2N4';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);