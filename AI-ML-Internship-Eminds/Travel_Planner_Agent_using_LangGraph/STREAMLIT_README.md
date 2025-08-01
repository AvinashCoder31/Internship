# 🌍 Travel Planner Agent - Streamlit Frontend

A beautiful, interactive Streamlit frontend for the AI-powered Travel Planner Agent built with LangGraph. This frontend provides an intuitive user interface for generating personalized travel plans with real-time weather data.

## ✨ Features

### 🎨 User Interface
- **Modern Design**: Clean, responsive interface with custom CSS styling
- **Interactive Sidebar**: Easy-to-use form controls for travel preferences
- **Tabbed Layout**: Organized display of travel plans, weather info, and export options
- **Real-time Feedback**: Loading spinners and status messages

### 🚀 Functionality
- **Destination Input**: Text input for any global destination
- **Budget Selection**: Choose from low, medium, or high budget ranges
- **Duration Setting**: Specify trip duration (1-30 days)
- **Interest Selection**: Multiple checkboxes for travel interests
- **Custom Interests**: Add personalized interests via text input
- **Real-time Weather**: Live weather data integration
- **Plan Generation**: AI-powered travel plan creation
- **File Operations**: Save and download travel plans
- **Copy to Clipboard**: Easy text copying functionality

## 🛠️ Installation & Setup

### Prerequisites
```bash
Python 3.8+
pip package manager
```

### 1. Install Dependencies
```bash
cd AI-ML-Internship-Eminds/Travel_Planner_Agent_using_LangGraph
pip install -r requirements.txt
```

### 2. Set Up API Keys
Create a `.env` file in the project root:
```bash
cp .env
```

Edit `.env` with your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
GEOAPIFY_API_KEY=your_geoapify_api_key_here
```

### 3. Run the Application
```bash
streamlit run streamlit_app.py
```

The application will open in your default browser at `http://localhost:8501`

## 🎯 How to Use

### Step 1: Enter Travel Details
1. **Destination**: Type your desired destination (e.g., "Paris", "Tokyo")
2. **Budget**: Select your budget range (low/medium/high)
3. **Duration**: Set the number of days for your trip
4. **Interests**: Check boxes for your interests or add custom ones

### Step 2: Generate Plan
1. Click the "🚀 Generate Travel Plan" button
2. Wait for the AI to process your request (with loading spinner)
3. View your personalized travel plan in the results area

### Step 3: Review Results
The results are organized in three tabs:

#### 📋 Travel Plan Tab
- Complete itinerary with day-by-day breakdown
- Activities organized by morning, afternoon, evening
- Budget considerations and cost estimates
- Travel tips and recommendations

#### 🌤️ Weather Info Tab
- Real-time weather conditions for your destination
- Temperature, weather description, and "feels like" temperature
- Weather-optimized recommendations

#### 💾 Save & Export Tab
- Automatic file saving (if enabled)
- Manual save button
- Download plan as Markdown file
- Copy plan text to clipboard

## 🏗️ Architecture

### Frontend Structure
```
streamlit_app.py
├── UI Components
│   ├── Header with gradient styling
│   ├── Sidebar with input forms
│   ├── Main content area
│   └── Footer with credits
├── Custom CSS Styling
│   ├── Gradient backgrounds
│   ├── Card layouts
│   ├── Button animations
│   └── Responsive design
└── Integration Layer
    ├── Service function imports
    ├── Error handling
    └── State management
```

### Backend Integration
The frontend directly imports and uses:
- [`generate_travel_plan()`](src/services/service1.py:237) - Main plan generation function
- [`save_travel_plan()`](src/services/service1.py:262) - File saving functionality

## 🎨 UI Components

### Sidebar Controls
- **Text Input**: Destination entry
- **Select Box**: Budget selection dropdown
- **Number Input**: Duration with min/max validation
- **Checkboxes**: Interest selection grid
- **Text Input**: Custom interests
- **Checkbox**: Save to file option
- **Button**: Generate plan trigger

### Main Display
- **Header**: Branded title with gradient background
- **Welcome Section**: Instructions and feature highlights
- **Results Tabs**: Organized plan display
- **Status Messages**: Success/error feedback
- **Loading Indicators**: Progress feedback

### Styling Features
- **Gradient Backgrounds**: Modern visual appeal
- **Card Layouts**: Organized information display
- **Hover Effects**: Interactive button animations
- **Responsive Design**: Works on different screen sizes
- **Color Coding**: Success (green), error (red), info (blue)

## 🔧 Customization

### Adding New Interests
To add more predefined interests, modify the checkbox section in [`streamlit_app.py`](streamlit_app.py:70):

```python
# Add new interests here
if st.checkbox("🎭 Theater"):
    interests.append("theater")
if st.checkbox("🏊 Swimming"):
    interests.append("swimming")
```

### Modifying Styling
Custom CSS is defined in the `st.markdown()` section at the top of [`main()`](streamlit_app.py:25). You can:
- Change color schemes
- Modify gradients
- Adjust spacing and sizing
- Add new component styles

### Extending Functionality
The modular design allows easy extension:
- Add new tabs for additional features
- Integrate more backend services
- Add data visualization components
- Implement user authentication

## 🚨 Error Handling

The application includes comprehensive error handling:

### API Key Validation
- Checks for missing environment variables
- Provides clear error messages for setup issues

### Input Validation
- Ensures destination is provided
- Validates interest selections
- Handles empty or invalid inputs gracefully

### Service Integration
- Catches backend service errors
- Displays user-friendly error messages
- Maintains application stability

## 📱 Mobile Responsiveness

The interface is designed to work on various screen sizes:
- **Desktop**: Full sidebar and main content
- **Tablet**: Responsive column layouts
- **Mobile**: Stacked components with touch-friendly controls

## 🔒 Security Considerations

- **API Keys**: Stored in environment variables, not in code
- **Input Sanitization**: User inputs are validated before processing
- **Error Messages**: Don't expose sensitive system information

## 🚀 Performance Features

- **Lazy Loading**: Components load as needed
- **Caching**: Streamlit's built-in caching for better performance
- **Efficient Rendering**: Minimal re-renders on state changes

## 🧪 Testing

### Manual Testing Checklist
- [ ] Application starts without errors
- [ ] All input fields work correctly
- [ ] Plan generation produces results
- [ ] Weather data displays properly
- [ ] File save/download functions work
- [ ] Error handling displays appropriate messages
- [ ] Responsive design works on different screen sizes

### Common Issues & Solutions

**Issue**: "Module not found" error
**Solution**: Ensure all dependencies are installed via `pip install -r requirements.txt`

**Issue**: API key errors
**Solution**: Verify `.env` file exists with correct API keys

**Issue**: Weather data not loading
**Solution**: Check WEATHER_API_KEY and GEOAPIFY_API_KEY validity

## 📈 Future Enhancements

### Planned Features
- **User Profiles**: Save user preferences and history
- **Multi-destination**: Support for multi-city trips
- **Budget Tracking**: Real-time cost calculations
- **Map Integration**: Visual destination mapping
- **Social Sharing**: Share plans on social media
- **PDF Export**: Professional PDF generation
- **Offline Mode**: Cached data for offline use

### Technical Improvements
- **Database Integration**: Persistent data storage
- **Authentication**: User login system
- **API Rate Limiting**: Prevent API quota exhaustion
- **Advanced Caching**: Redis or similar for better performance
- **Monitoring**: Application performance tracking

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Maintain consistent indentation

## 📄 License

This project is licensed under the MIT License - see the main project README for details.

## 🆘 Support

For issues and questions:
1. Check this documentation first
2. Review the main project README
3. Check existing issues in the repository
4. Create a new issue with detailed description

---

**Built with**: Streamlit 🎈 | LangGraph 🕸️ | Real-time APIs 🌐

**Perfect for**: Travel enthusiasts who want AI-powered, personalized trip planning with a beautiful interface!