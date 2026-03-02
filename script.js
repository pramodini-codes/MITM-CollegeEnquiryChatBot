/* script.js
   Robust chat frontend logic: message sending, file attach, previews, thinking indicator.
*/

const chatBody = document.querySelector(".chat-body");
const messageInput = document.querySelector(".message-input");
const sendMessageButton = document.querySelector("#send-message");
const fileInput = document.querySelector("#file-input");
const fileUploadButton = document.querySelector("#file-upload");

// API (adjust if needed)
const API_URL = "http://127.0.0.1:8000/chat";

// State for current outgoing message
const userData = {
  message: "",
  file: {
    data: null,       // base64 string (no data: prefix)
    mime_type: null,  // e.g. "image/png"
    dataUrl: null,    // data:image/...;base64,... (for preview)
    name: null
  }
};

let isSending = false;

// Utility: create message element
const createMessageElement = (contentHtml, ...classes) => {
  const div = document.createElement("div");
  div.classList.add("message", ...classes);
  div.innerHTML = contentHtml;
  return div;
};

// Utility: scroll chat to bottom
const scrollToBottom = (smooth = true) => {
  try {
    chatBody.scrollTo({
      top: chatBody.scrollHeight,
      behavior: smooth ? "smooth" : "auto"
    });
  } catch (err) {
    chatBody.scrollTop = chatBody.scrollHeight;
  }
};

// Show a bot "thinking" bubble and return the element
const appendThinkingBubble = () => {
  const thinkingHTML = `
    <svg class="bot-avatar" xmlns="http://www.w3.org/2000/svg" width="50" height="50">
      <circle cx="25" cy="25" r="20" fill="#444"/>
    </svg>
    <div class="message-text">
      <div class="thinking-indicator">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
      </div>
    </div>
  `;
  const thinkingDiv = createMessageElement(thinkingHTML, "bot-message", "thinking");
  chatBody.appendChild(thinkingDiv);
  scrollToBottom();
  return thinkingDiv;
};

// Replace thinking dots with real bot text
const writeBotReply = (thinkingDiv, text) => {
  const msgText = thinkingDiv.querySelector(".message-text");
  if (msgText) msgText.innerText = text;
  thinkingDiv.classList.remove("thinking");
  scrollToBottom();
};

// Generate bot response (posts to backend)
const generateBotResponse = async () => {
  if (isSending) return;
  isSending = true;
  sendMessageButton.disabled = true;
  fileUploadButton.disabled = true;
  messageInput.disabled = true;

  const thinkingDiv = appendThinkingBubble();

  try {
    // Build payload
    const payload = {
      message: userData.message || null,
      file: userData.file.data ? { data: userData.file.data, mime_type: userData.file.mime_type, name: userData.file.name } : null
    };

    // Post to the API
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      // Attempt to read JSON error if available
      let errText = `Server responded ${res.status}`;
      try {
        const j = await res.json();
        if (j && j.error) errText = j.error;
      } catch {}
      throw new Error(errText);
    }

    const data = await res.json();
    const reply = data && data.reply ? data.reply : "No reply.";

    writeBotReply(thinkingDiv, reply);
  } catch (err) {
    console.error("Error fetching bot reply:", err);
    writeBotReply(thinkingDiv, `❌ Error: ${err.message}`);
  } finally {
    // Reset UI state
    isSending = false;
    sendMessageButton.disabled = false;
    fileUploadButton.disabled = false;
    messageInput.disabled = false;

    // Reset stored userData.file after sending (keep message field cleared)
    userData.message = "";
    userData.file = { data: null, mime_type: null, dataUrl: null, name: null };
  }
};

// Handle sending a message (append user bubbles and call backend)
const handleOutgoingMessage = (ev) => {
  if (ev && typeof ev.preventDefault === "function") ev.preventDefault();
  if (isSending) return;

  // Trim current input
  const text = messageInput.value.trim();
  // Do not allow empty send unless a file is attached
  if (!text && !userData.file.data) return;

  // Append user message bubble if text present
  if (text) {
    const userBubble = createMessageElement(`<div class="message-text">${escapeHtml(text)}</div>`, "user-message");
    chatBody.appendChild(userBubble);
  }

  // Append file preview bubble if a file is attached
  if (userData.file.dataUrl) {
    const previewHtml = `
      <div class="message-text file-preview">
        <div class="file-meta">
          <div class="thumb-wrapper">
            <img src="${userData.file.dataUrl}" alt="${escapeHtml(userData.file.name || "file")}" class="file-thumb" />
          </div>
          <div class="file-info">
            <div class="file-name">${escapeHtml(userData.file.name || "attachment")}</div>
            <div class="file-type">${escapeHtml(userData.file.mime_type)}</div>
          </div>
        </div>
      </div>
    `;
    const fileBubble = createMessageElement(previewHtml, "user-message");
    chatBody.appendChild(fileBubble);
  }

  scrollToBottom();

  // move message text to state and clear input immediately (UX)
  userData.message = text;
  messageInput.value = "";

  // Call backend
  generateBotResponse();
};

// Simple HTML escape to prevent injection in inserted HTML
function escapeHtml(unsafe) {
  if (unsafe == null) return "";
  return String(unsafe)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// File input handler
fileInput.addEventListener("change", (e) => {
  const file = fileInput.files && fileInput.files[0];
  if (!file) return;

  // Accept only images (if you want other types remove this check)
  if (!file.type.startsWith("image/")) {
    console.warn("Only image attachments supported for preview. File accepted but no preview will show.");
  }

  const reader = new FileReader();
  reader.onload = (ev) => {
    const dataUrl = ev.target.result; // "data:<mime>;base64,...."
    const base64 = dataUrl.split(",")[1];

    userData.file = {
      data: base64,
      mime_type: file.type,
      dataUrl,
      name: file.name
    };

    console.log("FILE ATTACHED", {
      name: file.name,
      type: file.type,
      size: file.size
    });

    // Optionally show a small in-form UI indicator (not required since we preview on send)
    // e.g., show filename near input (left for CSS / extra UI)
  };

  reader.onerror = (err) => {
    console.error("FileReader error", err);
  };

  reader.readAsDataURL(file);

  // Clear the native input value so same file can be re-attached later if needed
  fileInput.value = "";
});

// Clicking the attach button triggers the hidden input
fileUploadButton.addEventListener("click", () => {
  if (isSending) return;
  fileInput.click();
});

// Submit on send button
sendMessageButton.addEventListener("click", (e) => {
  handleOutgoingMessage(e);
});

// Handle Enter to send (Shift+Enter for newline)
messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleOutgoingMessage(e);
  }
});

// Optional: prevent the form's natural submit if button is inside form
// (if your send button is type="submit", intercept form submit)
const maybeForm = document.querySelector(".chat-form");
if (maybeForm) {
  maybeForm.addEventListener("submit", (e) => {
    e.preventDefault();
    handleOutgoingMessage(e);
  });
}

// Initialize: focus textarea
messageInput.focus();
scrollToBottom(false);
