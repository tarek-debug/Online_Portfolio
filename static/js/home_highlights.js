
  // Define an empty object to hold the fetched project data
  let projectData = {};

  function fetchProjects() {
    fetch('/get_projects')
      .then(response => response.json())
      .then(data => {
        // Handle the fetched data here and update the projectData variable
        projectData = data;
      })
      .catch(error => console.error('Error fetching projects:', error));
  }
    // Get all the skill tags
    const skillTags = document.querySelectorAll('.skill-tag');
        
    const skillTitle = document.querySelector('.skill-title');
    const skillDescription = document.querySelector('.skill-description');
    const skillDetails = document.querySelector('.skill-details');
  
  
    // Function to retrieve project data based on the selected skill tag
    function getProjectsByTag(tag) {
      // Retrieve the project data for the selected tag from the projectData object
      console.log(projectData[tag]);
      return projectData[tag] || [];
    }
  
    // Add click event listeners to each skill tag
    skillTags.forEach((tag) => {
      tag.addEventListener('click', () => {
        const skill = tag.textContent;
        const isActive = tag.classList.contains('active');
  
        // Collapse previously expanded skill details if any
        const activeTag = document.querySelector('.skill-tag.active');
        if (activeTag && activeTag !== tag) {
          activeTag.classList.remove('active');
          skillDetails.style.display = 'none';
        }
  
        // Toggle the active class on the clicked skill tag
        tag.classList.toggle('active');
  
        // Check if the skill tag is active
        if (isActive) {
          // Collapse the skill details
          skillDetails.style.display = 'none';
        } else {
          // Expand the skill details
          skillTitle.textContent = skill;
          skillDescription.textContent = getSkillDescription(skill);
  
          // Retrieve the projects for the selected tag
          const projects = getProjectsByTag(skill);
  
          let timelineHTML = '';

          if (projects.length > 0) { // If there are projects for the selected tag
            // Generate the timeline HTML for the projects
            timelineHTML = projects.map(project => `
              <div class="timeline-item">
                <div class="timeline-icon">
                <img src="${project.imagePath}" alt="${project.title}"> <!-- Updated to use the imagePath from the data -->
                </div>
                <div class="timeline-content">
                  <h3>${project.title}</h3>
                  <p>${project.description}</p>
                  <a href="${project.detailsURL}">View details</a>
                </div>
              </div>
            `).join('');
          } else { // If no projects are found for the selected tag
            timelineHTML = '<p>Coming Soon</p>';
          }
      
          // Update the skill details HTML with the timeline or "Coming Soon"
          skillDetails.innerHTML = timelineHTML;
      
          skillDetails.style.display = 'block';
      
        }
      });
    });
  
    // Function to retrieve skill description based on skill name
    function getSkillDescription(skill) {
    }
  
  
  // Trigger the fetch function to load projects on page load
  fetchProjects();
  