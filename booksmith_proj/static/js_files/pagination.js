const contentContainer = document.getElementById("book-content");
let currentPage = 1;
const pageSize = 500; // Approximate character count per page
let pages = [];

// Initialize pagination by splitting content by paragraphs
function initializePagination() {
  // Get full content and split by paragraphs
  const fullContent = contentContainer.innerText.trim();
  const paragraphs = fullContent.split("\n");

  // Group paragraphs into pages
  let pageContent = "";
  paragraphs.forEach((paragraph) => {
    if ((pageContent + paragraph).length <= pageSize) {
      pageContent += paragraph + "\n";
    } else {
      pages.push(pageContent.trim());
      pageContent = paragraph + "\n";
    }
  });
  if (pageContent) pages.push(pageContent.trim());

  // Set the total pages and display the first page
  totalPages = pages.length;
  showPage(currentPage);
}

// Update page counter display
function updatePageCounter() {
  document.getElementById("current-page").textContent = currentPage;
  document.getElementById("total-pages").textContent = totalPages;
}

// Display the specified page content
function showPage(page) {
  contentContainer.innerText = pages[page - 1];

  // Disable buttons at boundaries
  document.getElementById("prev-btn").disabled = page === 1;
  document.getElementById("next-btn").disabled = page === totalPages;

  updatePageCounter();
}

// Navigate to the next page
function nextPage() {
  if (currentPage < totalPages) {
    currentPage++;
    showPage(currentPage);
  }
}

// Navigate to the previous page
function prevPage() {
  if (currentPage > 1) {
    currentPage--;
    showPage(currentPage);
  }
}

// Initialize pagination and set up keyboard navigation
document.addEventListener("DOMContentLoaded", () => {
  initializePagination();

  // Add keyboard navigation
  document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight") {
      nextPage();
    } else if (event.key === "ArrowLeft") {
      prevPage();
    }
  });
});
