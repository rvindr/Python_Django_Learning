const baseUrl = 'http://127.0.0.1:8000/api/blogs/';
let currentPage = 1;
let searchQuery = '';
let totalPages = 1;

const fetchBlogs = (page = 1, search = '') => {
  const url = new URL(baseUrl);
  url.searchParams.append('page', page);
  if (search) {
    url.searchParams.append('search', search);
  }

  fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    }
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      const blogContainer = document.getElementById('blog-container');
      blogContainer.innerHTML = '';  // Clear existing content

      // Populate the blog container with fetched blogs
      data.data.forEach(blog => {
        const blogSection = document.createElement('section');
        blogSection.className = 'pt-8 pt-xl-9';

        const rowDiv = document.createElement('div');
        rowDiv.className = 'row g-4 g-lg-6';

        const titleDiv = document.createElement('div');
        titleDiv.className = 'col-lg-8 mx-auto text-center';

        const blogTitle = document.createElement('h1');
        blogTitle.className = 'h2 mb-0';
        blogTitle.textContent = blog.title;

        titleDiv.appendChild(blogTitle);

        const innerRowDiv = document.createElement('div');
        innerRowDiv.className = 'row justify-content-between mt-4';

        const imgDiv = document.createElement('div');
        imgDiv.className = 'col-md-8 mx-auto text-center';  // Adjusted for responsiveness

        const blogImage = document.createElement('img');
        blogImage.src = blog.main_img;
        blogImage.className = 'img-fluid rounded';
        blogImage.alt = 'blog-img';

        imgDiv.appendChild(blogImage);

        const contentDiv = document.createElement('div');
        contentDiv.className = 'col-md-4 mx-auto my-auto';

        const blogText = document.createElement('p');
        blogText.textContent = blog.blog_text;

        contentDiv.appendChild(blogText);

        innerRowDiv.appendChild(imgDiv);
        innerRowDiv.appendChild(contentDiv);

        rowDiv.appendChild(titleDiv);
        rowDiv.appendChild(innerRowDiv);

        blogSection.appendChild(rowDiv);

        blogContainer.appendChild(blogSection);
      });

      // Update total pages and pagination controls
      totalPages = data.total_pages;
      updatePaginationControls(page);
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
};

// Update pagination controls
const updatePaginationControls = (page) => {
  const prevPageButton = document.getElementById('prev-page');
  const nextPageButton = document.getElementById('next-page');

  prevPageButton.disabled = (page <= 1);
  nextPageButton.disabled = (page >= totalPages);
};

// Initial fetch on page load
document.addEventListener('DOMContentLoaded', () => {
  fetchBlogs(currentPage, searchQuery);

  // Event listener for search input
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (event) => {
      searchQuery = event.target.value;
      fetchBlogs(currentPage, searchQuery);
    });
  }

  // Event listener for pagination controls
  const nextPageButton = document.getElementById('next-page');
  const prevPageButton = document.getElementById('prev-page');

  if (nextPageButton) {
    nextPageButton.addEventListener('click', () => {
      if (currentPage < totalPages) {
        currentPage++;
        fetchBlogs(currentPage, searchQuery);
      }
    });
  }

  if (prevPageButton) {
    prevPageButton.addEventListener('click', () => {
      if (currentPage > 1) {
        currentPage--;
        fetchBlogs(currentPage, searchQuery);
      }
    });
  }
});
