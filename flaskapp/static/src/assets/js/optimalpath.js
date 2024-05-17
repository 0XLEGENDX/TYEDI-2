const imageInput = document.getElementById('image-input');
const submitButton = document.getElementById('submit-button');
const imageContainer = document.getElementById('image-container');
let image = null;
let point1 = null;
let point2 = null;

imageInput.addEventListener('change', (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = (event) => {
    image = new Image();
    image.onload = () => {
      imageContainer.innerHTML = '';
      imageContainer.appendChild(image);
      point1 = createPoint(0, 0);
      point2 = createPoint(image.width, image.height);
      imageContainer.appendChild(point1);
      imageContainer.appendChild(point2);
    };
    image.src = event.target.result;
  };
  reader.readAsDataURL(file);
});

submitButton.addEventListener('click', () => {
  if (image && point1 && point2) {
    const formData = new FormData();
    formData.append('image', image);
    formData.append('point1_x', point1.style.left);
    formData.append('point1_y', point1.style.top);
    formData.append('point2_x', point2.style.left);
    formData.append('point2_y', point2.style.top);
    console.log(point1.style.left , point1.style.top);
    // Send form data using XMLHttpRequest or fetch API
  }
});

function createPoint(x, y) {
  const point = document.createElement('div');
  point.id = 'point-1';
  point.style.left = `${x}px`;
  point.style.top = `${y}px`;
  point.addEventListener('mousedown', (event) => {
    const movePoint = (moveEvent) => {
      point.style.left = `${moveEvent.clientX - imageContainer.offsetLeft - point.offsetWidth / 2}px`;
      point.style.top = `${moveEvent.clientY - imageContainer.offsetTop - point.offsetHeight / 2}px`;
    };
    const upPoint = () => {
      document.removeEventListener('mousemove', movePoint);
      document.removeEventListener('mouseup', upPoint);
    };
    document.addEventListener('mousemove', movePoint);
    document.addEventListener('mouseup', upPoint);
  });
  return point;
}