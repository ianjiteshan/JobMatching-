import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import Layout from './Layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  ArrowLeft,
  Target,
  Star,
  MapPin,
  Phone,
  Mail,
  GraduationCap,
  Briefcase,
  RefreshCw,
  Download,
  Eye,
  CheckCircle,
  XCircle
} from 'lucide-react'
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'

const CandidateMatching = ({ user, onLogout, apiBaseUrl }) => {
  const { jobId } = useParams()
  const [jobPosting, setJobPosting] = useState(null)
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)

  // Mock job posting data
  const mockJobPosting = {
    id: 1,
    title: 'Solar Panel Installation Technician',
    description: 'We are looking for skilled solar panel installation technicians to join our growing team.',
    city: 'Coimbatore',
    state: 'TAMIL NADU',
    salary_min: 18000,
    salary_max: 30000,
    experience_required: 1,
    minimum_diploma_score: 75.0,
    required_skills: ['Solar Panel Installation', 'Electrical Wiring', 'Safety Protocols'],
    preferred_skills: ['System Maintenance', 'Quality Control'],
    status: 'active'
  }

  // Mock matches data
  const mockMatches = [
    {
      job_seeker_id: 1,
      match_score: 0.945,
      match_percentage: 94.5,
      reasons: [
        'Excellent skills match (95%)',
        'Same location (Coimbatore)',
        'Salary expectations align',
        'High diploma score (95.0)',
        'Relevant experience (2 years)'
      ],
      candidate: {
        id: 1,
        name: 'Ramya Nithya Sri S L',
        phone_number: '+91-9876543210',
        email: 'ramya.nithya@email.com',
        city: 'Coimbatore',
        state: 'TAMIL NADU',
        qualifications: 'ITI in Solar Technology',
        diploma_score: 95.00,
        experience_years: 2,
        category: 'Gen',
        gender: 'Female',
        training_result: 'Pass',
        placement_status: 'Available',
        skills: ['Solar Panel Installation', 'Electrical Wiring', 'System Maintenance', 'Safety Protocols']
      },
      score_breakdown: {
        skills: 95.0,
        location: 100.0,
        salary: 90.0,
        experience: 95.0,
        diploma: 95.0
      }
    },
    {
      job_seeker_id: 2,
      match_score: 0.928,
      match_percentage: 92.8,
      reasons: [
        'Strong skills match (92%)',
        'Same location (Coimbatore)',
        'Salary expectations align',
        'High diploma score (94.37)',
        'Good experience (3 years)'
      ],
      candidate: {
        id: 2,
        name: 'Krishna Moorthi D',
        phone_number: '+91-9876543211',
        email: 'krishna.moorthi@email.com',
        city: 'Coimbatore',
        state: 'TAMIL NADU',
        qualifications: 'Diploma in Electrical Engineering',
        diploma_score: 94.37,
        experience_years: 3,
        category: 'OBC',
        gender: 'Male',
        training_result: 'Pass',
        placement_status: 'Available',
        skills: ['Solar Installation', 'Electrical Systems', 'Project Management', 'Safety Protocols']
      },
      score_breakdown: {
        skills: 92.0,
        location: 100.0,
        salary: 88.0,
        experience: 100.0,
        diploma: 94.0
      }
    },
    {
      job_seeker_id: 3,
      match_score: 0.912,
      match_percentage: 91.2,
      reasons: [
        'Good skills match (88%)',
        'Same location (Coimbatore)',
        'Salary expectations align',
        'Excellent diploma score (94.70)',
        'Adequate experience (1 year)'
      ],
      candidate: {
        id: 3,
        name: 'Kavitha M',
        phone_number: '+91-9876543212',
        email: 'kavitha.m@email.com',
        city: 'Coimbatore',
        state: 'TAMIL NADU',
        qualifications: 'ITI in Electronics',
        diploma_score: 94.70,
        experience_years: 1,
        category: 'SC',
        gender: 'Female',
        training_result: 'Pass',
        placement_status: 'Available',
        skills: ['Solar Panel Maintenance', 'Electronics', 'Quality Control', 'Safety Protocols']
      },
      score_breakdown: {
        skills: 88.0,
        location: 100.0,
        salary: 92.0,
        experience: 85.0,
        diploma: 95.0
      }
    }
  ]

  useEffect(() => {
    fetchJobAndMatches()
  }, [jobId])

  const fetchJobAndMatches = async () => {
    setLoading(true)
    try {
      // For demo, use mock data
      setTimeout(() => {
        setJobPosting(mockJobPosting)
        setMatches(mockMatches)
        setLoading(false)
      }, 1000)
    } catch (error) {
      console.error('Error fetching job and matches:', error)
      setJobPosting(mockJobPosting)
      setMatches(mockMatches)
      setLoading(false)
    }
  }

  const generateMatches = async () => {
    setGenerating(true)
    try {
      // Simulate ML matching process
      setTimeout(() => {
        setMatches(mockMatches)
        setGenerating(false)
      }, 3000)
    } catch (error) {
      console.error('Error generating matches:', error)
      setGenerating(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-600'
    if (score >= 80) return 'text-yellow-600'
    if (score >= 70) return 'text-orange-600'
    return 'text-red-600'
  }

  const getScoreBarColor = (score) => {
    if (score >= 90) return 'bg-green-500'
    if (score >= 80) return 'bg-yellow-500'
    if (score >= 70) return 'bg-orange-500'
    return 'bg-red-500'
  }

  if (loading) {
    return (
      <Layout user={user} onLogout={onLogout}>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout user={user} onLogout={onLogout}>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Button variant="outline" size="sm" asChild>
              <Link to="/employer/jobs">
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back to Jobs
              </Link>
            </Button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Candidate Matches</h1>
              <p className="text-gray-600">{jobPosting?.title}</p>
            </div>
          </div>
          <div className="flex space-x-3">
            <Button variant="outline" onClick={fetchJobAndMatches}>
              <RefreshCw className="mr-2 h-4 w-4" />
              Refresh
            </Button>
            <Button variant="outline">
              <Download className="mr-2 h-4 w-4" />
              Export
            </Button>
            <Button onClick={generateMatches} disabled={generating}>
              <Target className="mr-2 h-4 w-4" />
              {generating ? 'Generating...' : 'Generate Matches'}
            </Button>
          </div>
        </div>

        {/* Job Summary */}
        <Card>
          <CardHeader>
            <CardTitle>Job Details</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm font-medium text-gray-900">Location</p>
                <p className="text-sm text-gray-600">{jobPosting?.city}, {jobPosting?.state}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Salary Range</p>
                <p className="text-sm text-gray-600">₹{jobPosting?.salary_min.toLocaleString()} - ₹{jobPosting?.salary_max.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Experience Required</p>
                <p className="text-sm text-gray-600">{jobPosting?.experience_required} years</p>
              </div>
            </div>
            <div className="mt-4">
              <p className="text-sm font-medium text-gray-900 mb-2">Required Skills</p>
              <div className="flex flex-wrap gap-2">
                {jobPosting?.required_skills.map((skill, index) => (
                  <Badge key={index} variant="secondary">{skill}</Badge>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Matches Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Matches</CardTitle>
              <Target className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{matches.length}</div>
              <p className="text-xs text-muted-foreground">
                Candidates evaluated: 47
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg Match Score</CardTitle>
              <Star className="h-4 w-4 text-yellow-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">
                {matches.length > 0 ? Math.round(matches.reduce((sum, match) => sum + match.match_percentage, 0) / matches.length) : 0}%
              </div>
              <p className="text-xs text-muted-foreground">
                Quality matches found
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Top Match</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">
                {matches.length > 0 ? Math.round(matches[0].match_percentage) : 0}%
              </div>
              <p className="text-xs text-muted-foreground">
                {matches.length > 0 ? matches[0].candidate.name : 'No matches yet'}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Candidate Matches */}
        <div className="space-y-4">
          {matches.map((match, index) => (
            <Card key={match.job_seeker_id} className="overflow-hidden">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                        <span className="text-lg font-bold text-blue-600">#{index + 1}</span>
                      </div>
                    </div>
                    <div>
                      <CardTitle className="text-lg">{match.candidate.name}</CardTitle>
                      <CardDescription>
                        <div className="flex items-center space-x-4 mt-1">
                          <div className="flex items-center">
                            <MapPin className="mr-1 h-4 w-4" />
                            {match.candidate.city}, {match.candidate.state}
                          </div>
                          <div className="flex items-center">
                            <GraduationCap className="mr-1 h-4 w-4" />
                            Score: {match.candidate.diploma_score}
                          </div>
                          <div className="flex items-center">
                            <Briefcase className="mr-1 h-4 w-4" />
                            {match.candidate.experience_years} years exp
                          </div>
                        </div>
                      </CardDescription>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`text-2xl font-bold ${getScoreColor(match.match_percentage)}`}>
                      {Math.round(match.match_percentage)}%
                    </div>
                    <p className="text-sm text-gray-500">Match Score</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="overview" className="w-full">
                  <TabsList className="grid w-full grid-cols-3">
                    <TabsTrigger value="overview">Overview</TabsTrigger>
                    <TabsTrigger value="breakdown">Score Breakdown</TabsTrigger>
                    <TabsTrigger value="contact">Contact</TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="overview" className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-medium text-sm text-gray-900 mb-2">Qualifications</h4>
                        <p className="text-sm text-gray-600">{match.candidate.qualifications}</p>
                      </div>
                      <div>
                        <h4 className="font-medium text-sm text-gray-900 mb-2">Category</h4>
                        <Badge variant="outline">{match.candidate.category}</Badge>
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="font-medium text-sm text-gray-900 mb-2">Skills</h4>
                      <div className="flex flex-wrap gap-2">
                        {match.candidate.skills.map((skill, skillIndex) => (
                          <Badge 
                            key={skillIndex} 
                            variant={jobPosting?.required_skills.includes(skill) ? "default" : "secondary"}
                          >
                            {skill}
                            {jobPosting?.required_skills.includes(skill) && (
                              <CheckCircle className="ml-1 h-3 w-3" />
                            )}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="font-medium text-sm text-gray-900 mb-2">Match Reasons</h4>
                      <ul className="space-y-1">
                        {match.reasons.map((reason, reasonIndex) => (
                          <li key={reasonIndex} className="text-sm text-gray-600 flex items-center">
                            <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                            {reason}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="breakdown" className="space-y-4">
                    <div className="space-y-3">
                      {Object.entries(match.score_breakdown).map(([category, score]) => (
                        <div key={category} className="space-y-1">
                          <div className="flex justify-between text-sm">
                            <span className="font-medium capitalize">{category}</span>
                            <span className={getScoreColor(score)}>{Math.round(score)}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${getScoreBarColor(score)}`}
                              style={{ width: `${score}%` }}
                            ></div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="contact" className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-3">
                        <div className="flex items-center space-x-3">
                          <Phone className="h-4 w-4 text-gray-400" />
                          <span className="text-sm">{match.candidate.phone_number}</span>
                        </div>
                        <div className="flex items-center space-x-3">
                          <Mail className="h-4 w-4 text-gray-400" />
                          <span className="text-sm">{match.candidate.email}</span>
                        </div>
                      </div>
                      <div className="space-y-3">
                        <p className="text-sm"><span className="font-medium">Gender:</span> {match.candidate.gender}</p>
                        <p className="text-sm"><span className="font-medium">Training Result:</span> {match.candidate.training_result}</p>
                      </div>
                    </div>
                  </TabsContent>
                </Tabs>
                
                <div className="flex justify-end space-x-3 mt-6 pt-4 border-t">
                  <Button variant="outline" size="sm">
                    <Eye className="mr-2 h-4 w-4" />
                    View Profile
                  </Button>
                  <Button size="sm">
                    Contact Candidate
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {matches.length === 0 && !generating && (
          <Card>
            <CardContent className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <Target className="mx-auto h-12 w-12" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No matches found</h3>
              <p className="text-gray-600 mb-6">Generate matches to find suitable candidates for this job posting.</p>
              <Button onClick={generateMatches}>
                <Target className="mr-2 h-4 w-4" />
                Generate Matches
              </Button>
            </CardContent>
          </Card>
        )}

        {generating && (
          <Card>
            <CardContent className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Generating Matches</h3>
              <p className="text-gray-600">Our AI is analyzing candidates and finding the best matches...</p>
            </CardContent>
          </Card>
        )}
      </div>
    </Layout>
  )
}

export default CandidateMatching

