import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

interface Project {
  id: string;
  name: string;
  clientName?: string;
  description?: string;
}

export default function Builder() {
  const router = useRouter();
  const { projectId } = router.query;
  
  const [project, setProject] = useState<Project | null>(null);
  const [prompt, setPrompt] = useState('');
  const [generatedContent, setGeneratedContent] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [editHistory, setEditHistory] = useState<any[]>([]);
  const [feedback, setFeedback] = useState('');
  const [rating, setRating] = useState(5);

  useEffect(() => {
    if (projectId) {
      fetchProject();
    }
  }, [projectId]);

  const fetchProject = async () => {
    try {
      const response = await fetch(`/api/projects-temp/${projectId}`);
      if (response.ok) {
        const data = await response.json();
        setProject(data);
        if (data.description) {
          setPrompt(data.description);
        }
      }
    } catch (error) {
      console.error('Error fetching project:', error);
    }
  };

  const handleGenerate = async () => {
    if (!prompt || !projectId) return;
    
    setIsGenerating(true);
    try {
      const response = await fetch('/api/generate-temp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          projectId,
          prompt,
          type: 'full_page',
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to generate website');
      }

      const data = await response.json();
      setGeneratedContent(data.content);
    } catch (error) {
      console.error('Error generating website:', error);
      alert(error instanceof Error ? error.message : 'Failed to generate website. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSaveEdit = async (editedContent: string, reason: string) => {
    if (!projectId) return;

    try {
      const response = await fetch(`/api/projects/${projectId}/edits`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          originalContent: generatedContent,
          editedContent,
          editType: 'content_change',
          reason,
        }),
      });

      if (response.ok) {
        setGeneratedContent(editedContent);
        const edit = await response.json();
        setEditHistory([edit, ...editHistory]);
      }
    } catch (error) {
      console.error('Error saving edit:', error);
    }
  };

  const handleSubmitFeedback = async () => {
    if (!projectId || !feedback) return;

    try {
      const response = await fetch(`/api/projects/${projectId}/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          type: 'general',
          content: feedback,
          rating,
          clientName: project?.clientName,
        }),
      });

      if (response.ok) {
        setFeedback('');
        alert('Feedback submitted successfully!');
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  const handlePreview = () => {
    const blob = new Blob([generatedContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    window.open(url, '_blank');
  };

  if (!project) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => router.push('/')}
            className="text-blue-600 hover:text-blue-700 mb-4 inline-block"
          >
            ← Back to Projects
          </button>
          <h1 className="text-3xl font-bold text-gray-900">{project.name}</h1>
          {project.clientName && (
            <p className="text-gray-600 mt-2">Client: {project.clientName}</p>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Generation Panel */}
          <div className="bg-white shadow-lg rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Generate Website</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Describe the website you want to build
                </label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  rows={6}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Create a modern landing page for a coffee shop with a hero section, menu showcase, and contact form..."
                />
              </div>

              <button
                onClick={handleGenerate}
                disabled={isGenerating || !prompt}
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-md font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isGenerating ? 'Generating...' : 'Generate Website'}
              </button>
            </div>

            {/* Feedback Section */}
            {generatedContent && (
              <div className="mt-8 border-t pt-6">
                <h3 className="text-lg font-semibold mb-4">Provide Feedback</h3>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Rating
                    </label>
                    <select
                      value={rating}
                      onChange={(e) => setRating(Number(e.target.value))}
                      className="w-full px-4 py-2 border border-gray-300 rounded-md"
                    >
                      {[5, 4, 3, 2, 1].map(num => (
                        <option key={num} value={num}>{num} Stars</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Feedback
                    </label>
                    <textarea
                      value={feedback}
                      onChange={(e) => setFeedback(e.target.value)}
                      rows={3}
                      className="w-full px-4 py-2 border border-gray-300 rounded-md"
                      placeholder="What do you think about the generated website?"
                    />
                  </div>

                  <button
                    onClick={handleSubmitFeedback}
                    disabled={!feedback}
                    className="w-full bg-green-600 text-white py-2 px-4 rounded-md font-medium hover:bg-green-700 disabled:bg-gray-400"
                  >
                    Submit Feedback
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Preview Panel */}
          <div className="bg-white shadow-lg rounded-lg p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Preview</h2>
              {generatedContent && (
                <div className="space-x-2">
                  <button
                    onClick={handlePreview}
                    className="bg-gray-600 text-white py-2 px-4 rounded-md text-sm hover:bg-gray-700"
                  >
                    Open in New Tab
                  </button>
                </div>
              )}
            </div>

            {generatedContent ? (
              <div className="border border-gray-300 rounded-md overflow-hidden">
                <iframe
                  srcDoc={generatedContent}
                  className="w-full h-[600px]"
                  title="Website Preview"
                  sandbox="allow-scripts"
                />
              </div>
            ) : (
              <div className="flex items-center justify-center h-[600px] bg-gray-100 rounded-md">
                <p className="text-gray-500">Generate a website to see the preview</p>
              </div>
            )}

            {/* Edit History */}
            {editHistory.length > 0 && (
              <div className="mt-6">
                <h3 className="text-lg font-semibold mb-3">Recent Edits</h3>
                <div className="space-y-2">
                  {editHistory.slice(0, 5).map((edit, index) => (
                    <div key={edit.id || index} className="text-sm text-gray-600">
                      <span className="font-medium">{edit.editType}</span>
                      {edit.reason && <span> - {edit.reason}</span>}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}