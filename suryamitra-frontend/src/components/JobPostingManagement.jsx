import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Layout from './Layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { Label } from '@/components/ui/label'
import { 
  Plus, 
  Edit, 
  Trash2, 
  Eye,
  Target,
  MapPin,
  DollarSign,
  Calendar,
  Briefcase,
  X
} from 'lucide-react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

const JobPostingManagement = ({ user, onLogout, apiBaseUrl }) => {
  const [jobPostings, setJobPostings] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    required_qualifications: '',
    city: '',
    state: '',
    salary_min: '',
    salary_max: '',
    experience_required: '',
    minimum_diploma_score: '',
    required_skills: [],
    preferred_skills: []
  })
  const [newSkill, setNewSkill] = useState('')

  // Mock data for demonstration
  const mockJobPostings = [
    {
      id: 1,
      title: 'Solar Panel Installation Technician',
      description: 'We are looking for skilled solar panel installation technicians to join our growing team. The ideal candidate will have experience in electrical work and solar technology.',
      required_qualifications: 'ITI in Electrical/Electronics or equivalent',
      city: 'Coimbatore',
      state: 'TAMIL NADU',
      salary_min: 18000,
      salary_max: 30000,
      experience_required: 1,
      minimum_diploma_score: 75.0,
      required_skills: ['Solar Panel Installation', 'Electrical Wiring', 'Safety Protocols'],
      preferred_skills: ['System Maintenance', 'Quality Control'],
      status: 'active',
      created_at: '2025-01-21T10:00:00Z'
    },
    {
      id: 2,
      title: 'Solar System Maintenance Engineer',
      description: 'Seeking experienced maintenance engineers for solar power systems. Responsible for troubleshooting, repairs, and preventive maintenance.',
      required_qualifications: 'Diploma in Electrical Engineering',
      city: 'Vijayawada',
      state: 'ANDHRA PRADESH',
      salary_min: 20000,
      salary_max: 35000,
      experience_required: 2,
      minimum_diploma_score: 80.0,
      required_skills: ['System Maintenance', 'Troubleshooting', 'Electrical Systems'],
      preferred_skills: ['Project Management', 'Technical Documentation'],
      status: 'active',
      created_at: '2025-01-21T10:00:00Z'
    }
  ]

  const states = [
    'TAMIL NADU',
    'ANDHRA PRADESH',
    'WEST BENGAL',
    'UTTAR PRADESH',
    'KARNATAKA',
    'MAHARASHTRA',
    'GUJARAT',
    'RAJASTHAN'
  ]

  const commonSkills = [
    'Solar Panel Installation',
    'Electrical Wiring',
    'System Maintenance',
    'Troubleshooting',
    'Safety Protocols',
    'Quality Control',
    'Project Management',
    'Technical Documentation',
    'Electrical Systems',
    'Electronics'
  ]

  useEffect(() => {
    fetchJobPostings()
  }, [])

  const fetchJobPostings = async () => {
    setLoading(true)
    try {
      // For demo, use mock data
      setTimeout(() => {
        setJobPostings(mockJobPostings)
        setLoading(false)
      }, 1000)
    } catch (error) {
      console.error('Error fetching job postings:', error)
      setJobPostings(mockJobPostings)
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      // For demo, just add to local state
      const newJob = {
        id: Date.now(),
        ...formData,
        salary_min: parseInt(formData.salary_min),
        salary_max: parseInt(formData.salary_max),
        experience_required: parseInt(formData.experience_required),
        minimum_diploma_score: parseFloat(formData.minimum_diploma_score),
        status: 'active',
        created_at: new Date().toISOString()
      }
      
      setJobPostings([newJob, ...jobPostings])
      setShowCreateDialog(false)
      resetForm()
    } catch (error) {
      console.error('Error creating job posting:', error)
    }
  }

  const resetForm = () => {
    setFormData({
      title: '',
      description: '',
      required_qualifications: '',
      city: '',
      state: '',
      salary_min: '',
      salary_max: '',
      experience_required: '',
      minimum_diploma_score: '',
      required_skills: [],
      preferred_skills: []
    })
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const addSkill = (skillType) => {
    if (newSkill.trim() && !formData[skillType].includes(newSkill.trim())) {
      setFormData({
        ...formData,
        [skillType]: [...formData[skillType], newSkill.trim()]
      })
      setNewSkill('')
    }
  }

  const removeSkill = (skillType, skillToRemove) => {
    setFormData({
      ...formData,
      [skillType]: formData[skillType].filter(skill => skill !== skillToRemove)
    })
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case 'active':
        return <Badge variant="success">Active</Badge>
      case 'inactive':
        return <Badge variant="secondary">Inactive</Badge>
      case 'closed':
        return <Badge variant="destructive">Closed</Badge>
      default:
        return <Badge variant="secondary">{status}</Badge>
    }
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
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Job Postings</h1>
            <p className="text-gray-600">Manage your job openings and find the right candidates</p>
          </div>
          <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                Create Job Posting
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>Create New Job Posting</DialogTitle>
                <DialogDescription>
                  Fill in the details for your new job opening
                </DialogDescription>
              </DialogHeader>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="md:col-span-2">
                    <Label htmlFor="title">Job Title</Label>
                    <Input
                      id="title"
                      name="title"
                      value={formData.title}
                      onChange={handleChange}
                      placeholder="e.g., Solar Panel Installation Technician"
                      required
                    />
                  </div>
                  
                  <div className="md:col-span-2">
                    <Label htmlFor="description">Job Description</Label>
                    <Textarea
                      id="description"
                      name="description"
                      value={formData.description}
                      onChange={handleChange}
                      placeholder="Describe the role, responsibilities, and requirements..."
                      rows={4}
                      required
                    />
                  </div>
                  
                  <div className="md:col-span-2">
                    <Label htmlFor="required_qualifications">Required Qualifications</Label>
                    <Textarea
                      id="required_qualifications"
                      name="required_qualifications"
                      value={formData.required_qualifications}
                      onChange={handleChange}
                      placeholder="e.g., ITI in Electrical/Electronics, Diploma in Engineering..."
                      rows={2}
                      required
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="city">City</Label>
                    <Input
                      id="city"
                      name="city"
                      value={formData.city}
                      onChange={handleChange}
                      placeholder="e.g., Coimbatore"
                      required
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="state">State</Label>
                    <Select value={formData.state} onValueChange={(value) => setFormData({...formData, state: value})}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select state" />
                      </SelectTrigger>
                      <SelectContent>
                        {states.map(state => (
                          <SelectItem key={state} value={state}>{state}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div>
                    <Label htmlFor="salary_min">Minimum Salary (₹)</Label>
                    <Input
                      id="salary_min"
                      name="salary_min"
                      type="number"
                      value={formData.salary_min}
                      onChange={handleChange}
                      placeholder="15000"
                      required
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="salary_max">Maximum Salary (₹)</Label>
                    <Input
                      id="salary_max"
                      name="salary_max"
                      type="number"
                      value={formData.salary_max}
                      onChange={handleChange}
                      placeholder="30000"
                      required
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="experience_required">Experience Required (years)</Label>
                    <Input
                      id="experience_required"
                      name="experience_required"
                      type="number"
                      value={formData.experience_required}
                      onChange={handleChange}
                      placeholder="1"
                      min="0"
                      required
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="minimum_diploma_score">Minimum Diploma Score</Label>
                    <Input
                      id="minimum_diploma_score"
                      name="minimum_diploma_score"
                      type="number"
                      step="0.1"
                      value={formData.minimum_diploma_score}
                      onChange={handleChange}
                      placeholder="75.0"
                      min="0"
                      max="100"
                    />
                  </div>
                </div>
                
                {/* Skills Section */}
                <div className="space-y-4">
                  <div>
                    <Label>Required Skills</Label>
                    <div className="flex space-x-2 mt-2">
                      <Input
                        value={newSkill}
                        onChange={(e) => setNewSkill(e.target.value)}
                        placeholder="Add a required skill..."
                        onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill('required_skills'))}
                      />
                      <Button type="button" onClick={() => addSkill('required_skills')}>Add</Button>
                    </div>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {formData.required_skills.map((skill, index) => (
                        <Badge key={index} variant="secondary" className="flex items-center gap-1">
                          {skill}
                          <X 
                            className="h-3 w-3 cursor-pointer" 
                            onClick={() => removeSkill('required_skills', skill)}
                          />
                        </Badge>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <Label>Preferred Skills (Optional)</Label>
                    <div className="flex space-x-2 mt-2">
                      <Input
                        value={newSkill}
                        onChange={(e) => setNewSkill(e.target.value)}
                        placeholder="Add a preferred skill..."
                        onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill('preferred_skills'))}
                      />
                      <Button type="button" onClick={() => addSkill('preferred_skills')}>Add</Button>
                    </div>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {formData.preferred_skills.map((skill, index) => (
                        <Badge key={index} variant="outline" className="flex items-center gap-1">
                          {skill}
                          <X 
                            className="h-3 w-3 cursor-pointer" 
                            onClick={() => removeSkill('preferred_skills', skill)}
                          />
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
                
                <div className="flex justify-end space-x-3 pt-4">
                  <Button type="button" variant="outline" onClick={() => setShowCreateDialog(false)}>
                    Cancel
                  </Button>
                  <Button type="submit">
                    Create Job Posting
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        {/* Job Postings List */}
        <div className="space-y-4">
          {jobPostings.map((job) => (
            <Card key={job.id}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg">{job.title}</CardTitle>
                    <CardDescription className="mt-1">
                      <div className="flex items-center space-x-4 text-sm">
                        <div className="flex items-center">
                          <MapPin className="mr-1 h-4 w-4" />
                          {job.city}, {job.state}
                        </div>
                        <div className="flex items-center">
                          <DollarSign className="mr-1 h-4 w-4" />
                          ₹{job.salary_min.toLocaleString()} - ₹{job.salary_max.toLocaleString()}
                        </div>
                        <div className="flex items-center">
                          <Briefcase className="mr-1 h-4 w-4" />
                          {job.experience_required} years exp
                        </div>
                        <div className="flex items-center">
                          <Calendar className="mr-1 h-4 w-4" />
                          {new Date(job.created_at).toLocaleDateString()}
                        </div>
                      </div>
                    </CardDescription>
                  </div>
                  <div className="flex items-center space-x-2">
                    {getStatusBadge(job.status)}
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <p className="text-gray-600 text-sm">{job.description}</p>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <h4 className="font-medium text-sm text-gray-900 mb-2">Required Skills</h4>
                      <div className="flex flex-wrap gap-1">
                        {job.required_skills.map((skill, index) => (
                          <Badge key={index} variant="secondary" className="text-xs">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    
                    {job.preferred_skills.length > 0 && (
                      <div>
                        <h4 className="font-medium text-sm text-gray-900 mb-2">Preferred Skills</h4>
                        <div className="flex flex-wrap gap-1">
                          {job.preferred_skills.map((skill, index) => (
                            <Badge key={index} variant="outline" className="text-xs">
                              {skill}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="flex items-center justify-between pt-4 border-t">
                    <div className="text-sm text-gray-600">
                      <span className="font-medium">Qualifications:</span> {job.required_qualifications}
                      {job.minimum_diploma_score && (
                        <span className="ml-4">
                          <span className="font-medium">Min Score:</span> {job.minimum_diploma_score}%
                        </span>
                      )}
                    </div>
                    
                    <div className="flex space-x-2">
                      <Button size="sm" variant="outline">
                        <Eye className="mr-2 h-4 w-4" />
                        View
                      </Button>
                      <Button size="sm" variant="outline">
                        <Edit className="mr-2 h-4 w-4" />
                        Edit
                      </Button>
                      <Button size="sm" variant="outline" asChild>
                        <Link to={`/employer/jobs/${job.id}/matches`}>
                          <Target className="mr-2 h-4 w-4" />
                          Find Matches
                        </Link>
                      </Button>
                      <Button size="sm" variant="outline">
                        <Trash2 className="mr-2 h-4 w-4" />
                        Delete
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {jobPostings.length === 0 && (
          <Card>
            <CardContent className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <Briefcase className="mx-auto h-12 w-12" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No job postings yet</h3>
              <p className="text-gray-600 mb-6">Create your first job posting to start finding candidates.</p>
              <Button onClick={() => setShowCreateDialog(true)}>
                <Plus className="mr-2 h-4 w-4" />
                Create Job Posting
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </Layout>
  )
}

export default JobPostingManagement

