// Mock data for demo purposes until backend integration

export const mockCompanies = {
  'Software Engineering': [
    {
      name: 'Google',
      logo: '🔍',
      website: 'https://careers.google.com',
      location: 'Bangalore, India',
      size: '100k+ employees',
      description: 'Leading technology company focusing on search, cloud computing, and AI innovations.',
      openRoles: 45
    },
    {
      name: 'Microsoft',
      logo: 'Ⓜ️',
      website: 'https://careers.microsoft.com',
      location: 'Hyderabad, India',
      size: '200k+ employees',
      description: 'Global technology company known for cloud services, productivity software, and enterprise solutions.',
      openRoles: 38
    },
    {
      name: 'Amazon',
      logo: '📦',
      website: 'https://amazon.jobs',
      location: 'Bangalore, India',
      size: '1.5M+ employees',
      description: 'E-commerce and cloud computing giant with opportunities in multiple tech domains.',
      openRoles: 67
    },
    {
      name: 'Flipkart',
      logo: '🛒',
      website: 'https://www.flipkartcareers.com',
      location: 'Bangalore, India',
      size: '50k+ employees',
      description: 'Leading Indian e-commerce platform with strong technology and innovation focus.',
      openRoles: 23
    },
    {
      name: 'Zomato',
      logo: '🍕',
      website: 'https://www.zomato.com/careers',
      location: 'Gurgaon, India',
      size: '5k+ employees',
      description: 'Food delivery and restaurant discovery platform with cutting-edge technology.',
      openRoles: 15
    },
    {
      name: 'Paytm',
      logo: '💳',
      website: 'https://careers.paytm.com',
      location: 'Noida, India',
      size: '10k+ employees',
      description: 'Digital payments and financial services company leveraging advanced technology.',
      openRoles: 28
    }
  ],
  'Data Science': [
    {
      name: 'Netflix',
      logo: '🎬',
      website: 'https://jobs.netflix.com',
      location: 'Mumbai, India',
      size: '11k+ employees',
      description: 'Streaming giant using advanced ML and data analytics for content recommendations.',
      openRoles: 12
    },
    {
      name: 'Uber',
      logo: '🚗',
      website: 'https://www.uber.com/careers',
      location: 'Bangalore, India',
      size: '26k+ employees',
      description: 'Mobility platform leveraging data science for route optimization and pricing.',
      openRoles: 18
    },
    {
      name: 'Swiggy',
      logo: '🍔',
      website: 'https://careers.swiggy.com',
      location: 'Bangalore, India',
      size: '3k+ employees',
      description: 'Food delivery platform using data science for demand forecasting and logistics.',
      openRoles: 8
    },
    {
      name: 'PhonePe',
      logo: '📱',
      website: 'https://www.phonepe.com/careers',
      location: 'Bangalore, India',
      size: '3k+ employees',
      description: 'Digital payments platform utilizing ML for fraud detection and risk management.',
      openRoles: 14
    },
    {
      name: 'Ola',
      logo: '🛺',
      website: 'https://www.olacabs.com/careers',
      location: 'Bangalore, India',
      size: '5k+ employees',
      description: 'Mobility solutions company using data analytics for dynamic pricing and operations.',
      openRoles: 9
    },
    {
      name: 'BYJU\'S',
      logo: '📚',
      website: 'https://byjus.com/careers',
      location: 'Bangalore, India',
      size: '50k+ employees',
      description: 'EdTech platform using data science for personalized learning and student analytics.',
      openRoles: 11
    }
  ],
  'Marketing': [
    {
      name: 'Unilever',
      logo: '🧴',
      website: 'https://careers.unilever.com',
      location: 'Mumbai, India',
      size: '190k+ employees',
      description: 'Global consumer goods company with strong focus on digital marketing innovation.',
      openRoles: 16
    },
    {
      name: 'Procter & Gamble',
      logo: '🏠',
      website: 'https://www.pgcareers.com',
      location: 'Mumbai, India',
      size: '100k+ employees',
      description: 'Consumer goods giant known for innovative marketing strategies and brand management.',
      openRoles: 12
    },
    {
      name: 'Coca-Cola',
      logo: '🥤',
      website: 'https://careers.coca-colacompany.com',
      location: 'Gurgaon, India',
      size: '86k+ employees',
      description: 'Global beverage company with opportunities in digital marketing and brand strategy.',
      openRoles: 8
    }
  ],
  'Finance': [
    {
      name: 'JPMorgan Chase',
      logo: '🏦',
      website: 'https://careers.jpmorgan.com',
      location: 'Mumbai, India',
      size: '280k+ employees',
      description: 'Leading global financial services firm with diverse career opportunities.',
      openRoles: 22
    },
    {
      name: 'Goldman Sachs',
      logo: '💰',
      website: 'https://www.goldmansachs.com/careers',
      location: 'Bangalore, India',
      size: '45k+ employees',
      description: 'Investment banking and financial services company known for innovation.',
      openRoles: 18
    },
    {
      name: 'HDFC Bank',
      logo: '🏛️',
      website: 'https://www.hdfcbank.com/careers',
      location: 'Mumbai, India',
      size: '150k+ employees',
      description: 'Leading Indian private sector bank with extensive career opportunities.',
      openRoles: 45
    }
  ]
};

export const mockImprovements = [
  {
    category: 'skills' as const,
    priority: 'high' as const,
    title: 'Add Technical Skills Section',
    description: 'Your resume lacks a dedicated technical skills section.',
    suggestion: 'Create a "Technical Skills" section highlighting programming languages, frameworks, and tools you\'ve used. Include proficiency levels.',
    impact: 'Can increase interview callbacks by 40% for technical roles'
  },
  {
    category: 'keywords' as const,
    priority: 'high' as const,
    title: 'Include Industry Keywords',
    description: 'Missing relevant industry-specific keywords that ATS systems look for.',
    suggestion: 'Incorporate keywords like "Agile methodology", "CI/CD", "cloud computing" naturally throughout your experience descriptions.',
    impact: 'Improves ATS screening success rate by 60%'
  },
  {
    category: 'experience' as const,
    priority: 'medium' as const,
    title: 'Quantify Your Achievements',
    description: 'Several achievements lack specific metrics or numbers.',
    suggestion: 'Add quantifiable results: "Improved system performance by 35%" instead of "Improved system performance".',
    impact: 'Makes accomplishments more compelling and memorable'
  },
  {
    category: 'format' as const,
    priority: 'medium' as const,
    title: 'Optimize Resume Length',
    description: 'Resume length could be better optimized for your experience level.',
    suggestion: 'Keep resume to 1-2 pages max. Focus on most relevant experiences from the last 10 years.',
    impact: 'Increases recruiter attention and readability'
  },
  {
    category: 'format' as const,
    priority: 'low' as const,
    title: 'Improve Visual Formatting',
    description: 'Resume formatting could be more professional and ATS-friendly.',
    suggestion: 'Use consistent fonts, proper spacing, and clear section headers. Avoid graphics and complex formatting.',
    impact: 'Ensures compatibility with ATS systems and improves readability'
  }
];

export const mockUniquenessResult = {
  overallScore: 23,
  matches: [
    {
      text: "Experienced software developer with strong analytical and problem-solving skills",
      similarity: 78,
      source: "Common resume templates",
      category: 'medium' as const
    },
    {
      text: "Responsible for developing and maintaining web applications",
      similarity: 65,
      source: "Generic job descriptions",
      category: 'medium' as const
    },
    {
      text: "Team player with excellent communication skills",
      similarity: 82,
      source: "Resume clichés database",
      category: 'low' as const
    }
  ],
  totalChecked: 45,
  cleanSentences: 42,
  flaggedSentences: 3
};