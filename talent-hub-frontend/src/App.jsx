import React, { useState, useEffect } from 'react';
import { Search, MapPin, Briefcase, Users, Plus, Filter, Menu, X, Star, DollarSign, Clock, Building2, User, Mail, Phone, Globe } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

const TalentHubPro = () => {
  const [userType, setUserType] = useState('jobseeker'); // 'jobseeker' or 'employer'
  const [view, setView] = useState('map'); // 'map' or 'list'
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    maxDistance: 50,
    minRating: 0,
    workMode: [],
    salaryMin: 0,
    salaryMax: 500000
  });

  const mapCenter = { lat: -34.6037, lng: -58.3816 };

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/api/rag/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: query,
          filters: filters,
          top_k: 20
        })
      });

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error:', error);
      alert('Error connecting to backend. Make sure server is running on http://localhost:8000');
    } finally {
      setLoading(false);
    }
  };

  const parseLocation = (location) => {
    if (typeof location === 'string') {
      try {
        return JSON.parse(location);
      } catch {
        return { city: location, distance: 0, lat: mapCenter.lat, lng: mapCenter.lng };
      }
    }
    return location || { city: 'Unknown', distance: 0, lat: mapCenter.lat, lng: mapCenter.lng };
  };

  const parseList = (value) => {
    if (Array.isArray(value)) return value;
    if (typeof value === 'string') {
      return value.split(',').map(v => v.trim()).filter(Boolean);
    }
    return [];
  };

  // Mock jobs data (you'll replace this with API calls later)
  const mockJobs = [
    {
      id: 1,
      title: "Senior React Developer",
      company: "TechCorp",
      location: { city: "Palermo, Buenos Aires", distance: 2.5, lat: -34.5889, lng: -58.4194 },
      salary: 350000,
      workMode: ["Híbrido"],
      description: "Looking for experienced React developer",
      skills: ["React", "TypeScript", "Node.js"],
      postedDate: "2 days ago"
    },
    {
      id: 2,
      title: "UX Designer",
      company: "Design Studio",
      location: { city: "Recoleta, Buenos Aires", distance: 3.2, lat: -34.5875, lng: -58.3974 },
      salary: 280000,
      workMode: ["Remoto"],
      description: "Creative UX designer needed",
      skills: ["Figma", "Adobe XD", "User Research"],
      postedDate: "1 week ago"
    },
    {
      id: 3,
      title: "Python Data Engineer",
      company: "DataCo",
      location: { city: "Microcentro, Buenos Aires", distance: 1.8, lat: -34.6037, lng: -58.3816 },
      salary: 400000,
      workMode: ["Presencial"],
      description: "Build data pipelines and analytics",
      skills: ["Python", "SQL", "AWS"],
      postedDate: "3 days ago"
    }
  ];

  const JobCard = ({ job }) => {
    const location = parseLocation(job.location);
    const skills = parseList(job.skills);
    const workMode = parseList(job.workMode);

    return (
      <div 
        onClick={() => setSelectedItem(job)}
        className="bg-white rounded-lg shadow-md hover:shadow-xl transition-all p-6 cursor-pointer border-l-4 border-blue-500"
      >
        <div className="flex justify-between items-start mb-3">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-gray-900 mb-1">{job.title}</h3>
            <div className="flex items-center gap-2 text-gray-600">
              <Building2 className="w-4 h-4" />
              <span className="font-medium">{job.company}</span>
            </div>
          </div>
          <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
            ${(job.salary / 1000).toFixed(0)}K
          </div>
        </div>

        <div className="space-y-2 mb-4">
          <div className="flex items-center gap-2 text-gray-600">
            <MapPin className="w-4 h-4 text-red-500" />
            <span className="text-sm">{location.city} • {location.distance} km away</span>
          </div>
          <div className="flex gap-2">
            {workMode.map((mode, i) => (
              <span key={i} className="bg-purple-100 text-purple-700 px-2 py-1 rounded text-xs font-medium">
                {mode}
              </span>
            ))}
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mb-3">
          {skills.slice(0, 4).map((skill, i) => (
            <span key={i} className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-xs">
              {skill}
            </span>
          ))}
        </div>

        <div className="text-sm text-gray-500 mt-3 pt-3 border-t">
          Posted {job.postedDate}
        </div>
      </div>
    );
  };

  const ProfessionalCard = ({ professional }) => {
    const location = parseLocation(professional.location);
    const skills = parseList(professional.skills);
    const workMode = parseList(professional.workMode);

    return (
      <div 
        onClick={() => setSelectedItem(professional)}
        className="bg-white rounded-lg shadow-md hover:shadow-xl transition-all p-6 cursor-pointer border-l-4 border-green-500"
      >
        <div className="flex justify-between items-start mb-3">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-gray-900 mb-1">{professional.name}</h3>
            <p className="text-blue-600 font-medium">{professional.title}</p>
          </div>
          <div className="flex items-center gap-1 bg-yellow-100 px-3 py-1 rounded-full">
            <Star className="w-4 h-4 text-yellow-500 fill-current" />
            <span className="font-bold">{professional.rating || 0}</span>
          </div>
        </div>

        <div className="space-y-2 mb-4">
          <div className="flex items-center gap-2 text-gray-600">
            <MapPin className="w-4 h-4 text-red-500" />
            <span className="text-sm">{location.city} • {location.distance} km away</span>
          </div>
          <div className="flex items-center gap-2 text-gray-600">
            <DollarSign className="w-4 h-4 text-green-500" />
            <span className="text-sm">${professional.salary}/month expected</span>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mb-3">
          {skills.slice(0, 4).map((skill, i) => (
            <span key={i} className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-xs">
              {skill}
            </span>
          ))}
        </div>

        <div className="flex gap-2 mt-3">
          {workMode.map((mode, i) => (
            <span key={i} className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs">
              {mode}
            </span>
          ))}
        </div>
      </div>
    );
  };

  const InteractiveMap = () => {
    const items = userType === 'jobseeker' ? mockJobs : (results?.professionals || []);
    
    return (
      <div className="bg-white rounded-xl shadow-lg overflow-hidden" style={{ height: '700px' }}>
        <div className="p-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <MapPin className="w-6 h-6" />
            {userType === 'jobseeker' ? 'Jobs in Buenos Aires' : 'Professionals in Buenos Aires'}
          </h2>
        </div>
        
        <div className="relative" style={{ height: 'calc(100% - 72px)' }}>
          {/* Map Container */}
          <div className="absolute inset-0 bg-gray-100 flex items-center justify-center">
            <iframe
              width="100%"
              height="100%"
              frameBorder="0"
              scrolling="no"
              marginHeight="0"
              marginWidth="0"
              src="https://www.openstreetmap.org/export/embed.html?bbox=-58.5316%2C-34.7052%2C-58.3316%2C-34.5052&amp;layer=mapnik&amp;marker=-34.6037%2C-58.3816"
              style={{ border: 0 }}
            ></iframe>
          </div>

          {/* Items Overlay */}
          <div className="absolute top-4 right-4 bg-white rounded-lg shadow-2xl p-4 w-80 max-h-[600px] overflow-y-auto">
            <h3 className="font-bold text-lg mb-3 flex items-center gap-2 text-gray-800">
              <MapPin className="w-5 h-5 text-red-500" />
              {items.length} {userType === 'jobseeker' ? 'Jobs' : 'Professionals'} Near You
            </h3>
            
            {items.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-500 text-sm">
                  {userType === 'jobseeker' 
                    ? 'No jobs available at the moment' 
                    : 'Search for professionals to see results here'}
                </p>
              </div>
            ) : (
              <div className="space-y-2">
                {items.map((item, index) => {
                  const location = parseLocation(item.location);
                  return (
                    <div
                      key={index}
                      onClick={() => setSelectedItem(item)}
                      className="flex items-start gap-3 p-3 bg-gradient-to-r from-blue-50 to-purple-50 hover:from-blue-100 hover:to-purple-100 rounded-lg cursor-pointer transition-all border border-blue-200"
                    >
                      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm flex-shrink-0">
                        {index + 1}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-bold text-gray-900 text-sm truncate">
                          {item.title || item.name}
                        </h4>
                        <p className="text-xs text-gray-600 truncate">
                          {item.company || item.title}
                        </p>
                        <div className="flex items-center gap-2 mt-1">
                          <MapPin className="w-3 h-3 text-red-500" />
                          <span className="text-xs text-gray-600">{location.city}</span>
                          <span className="text-xs text-blue-600 font-medium">{location.distance} km</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold flex items-center gap-2">
                <Briefcase className="w-8 h-8" />
                TalentHub Pro
              </h1>
              <p className="text-blue-100 text-sm mt-1">AI-Powered Job & Talent Matching</p>
            </div>
            
            {/* User Type Toggle */}
            <div className="flex gap-2 bg-white/20 rounded-lg p-1">
              <button
                onClick={() => setUserType('jobseeker')}
                className={`px-4 py-2 rounded-md font-medium transition-all flex items-center gap-2 ${
                  userType === 'jobseeker'
                    ? 'bg-white text-blue-600 shadow-md'
                    : 'text-white hover:bg-white/10'
                }`}
              >
                <User className="w-4 h-4" />
                Find Jobs
              </button>
              <button
                onClick={() => setUserType('employer')}
                className={`px-4 py-2 rounded-md font-medium transition-all flex items-center gap-2 ${
                  userType === 'employer'
                    ? 'bg-white text-blue-600 shadow-md'
                    : 'text-white hover:bg-white/10'
                }`}
              >
                <Building2 className="w-4 h-4" />
                Find Talent
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Search Bar */}
      <div className="bg-white shadow-md border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder={
                  userType === 'jobseeker'
                    ? "Search jobs: 'React developer remote' or 'UX designer Buenos Aires'..."
                    : "Search talent: 'Python developer with AWS experience'..."
                }
                className="w-full pl-12 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
              />
            </div>
            
            {/* View Toggle */}
            <div className="flex gap-2 bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setView('map')}
                className={`px-4 py-2 rounded-md font-medium transition-all ${
                  view === 'map'
                    ? 'bg-white shadow-md text-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Map
              </button>
              <button
                onClick={() => setView('list')}
                className={`px-4 py-2 rounded-md font-medium transition-all ${
                  view === 'list'
                    ? 'bg-white shadow-md text-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                List
              </button>
            </div>

            <button
              onClick={() => setShowFilters(!showFilters)}
              className="px-6 py-3 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium flex items-center gap-2 transition-all"
            >
              <Filter className="w-5 h-5" />
              Filters
            </button>

            <button
              onClick={handleSearch}
              disabled={loading}
              className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-bold hover:from-blue-700 hover:to-purple-700 transition-all shadow-md disabled:opacity-50"
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </div>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div className="bg-blue-50 border-b">
          <div className="container mx-auto px-4 py-4">
            <div className="grid grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Max Distance: {filters.maxDistance} km
                </label>
                <input
                  type="range"
                  min="5"
                  max="100"
                  value={filters.maxDistance}
                  onChange={(e) => setFilters({...filters, maxDistance: parseInt(e.target.value)})}
                  className="w-full"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Min Rating: {filters.minRating}
                </label>
                <input
                  type="range"
                  min="0"
                  max="5"
                  step="0.5"
                  value={filters.minRating}
                  onChange={(e) => setFilters({...filters, minRating: parseFloat(e.target.value)})}
                  className="w-full"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Work Mode</label>
                <div className="flex gap-2">
                  {['Remote', 'Hybrid', 'Onsite'].map(mode => (
                    <label key={mode} className="flex items-center gap-1 text-sm">
                      <input
                        type="checkbox"
                        checked={filters.workMode.includes(mode)}
                        onChange={(e) => {
                          const newModes = e.target.checked
                            ? [...filters.workMode, mode]
                            : filters.workMode.filter(m => m !== mode);
                          setFilters({...filters, workMode: newModes});
                        }}
                        className="w-4 h-4"
                      />
                      {mode}
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="container mx-auto px-4 py-6">
        {view === 'map' ? (
          <InteractiveMap />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {userType === 'jobseeker' ? (
              mockJobs.length > 0 ? (
                mockJobs.map((job) => <JobCard key={job.id} job={job} />)
              ) : (
                <div className="col-span-full text-center py-20">
                  <Briefcase className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-xl font-bold text-gray-600 mb-2">No jobs found</h3>
                  <p className="text-gray-500">Try adjusting your search or filters</p>
                </div>
              )
            ) : results?.professionals && results.professionals.length > 0 ? (
              results.professionals.map((prof, idx) => (
                <ProfessionalCard key={idx} professional={prof} />
              ))
            ) : (
              <div className="col-span-full text-center py-20 bg-white rounded-xl shadow-md">
                <Users className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-gray-600 mb-2">
                  {userType === 'jobseeker' ? 'Find Your Dream Job' : 'Find Top Talent'}
                </h3>
                <p className="text-gray-500 mb-4">
                  {userType === 'jobseeker'
                    ? 'Click "Map" to see job locations or search for specific positions'
                    : 'Search for professionals by skills, experience, or location'}
                </p>
                <button
                  onClick={() => setView('map')}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-all inline-flex items-center gap-2"
                >
                  <MapPin className="w-5 h-5" />
                  View on Map
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default TalentHubPro;