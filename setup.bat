@echo off
echo 🚀 Setting up AskMe Flask Backend...
echo.

echo 📦 Installing Python dependencies...
pip install -r requirements.txt
echo.

echo ✅ Dependencies installed!
echo.

echo 🔧 Next steps:
echo 1. Go to your Supabase dashboard
echo 2. Open the SQL editor
echo 3. Run the SQL from setup_database.sql
echo 4. If you encounter issues, run reset_database.sql first
echo 5. Then run: python api.py
echo 6. Test with: python test_api.py
echo.

pause
