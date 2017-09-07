var dragging = 0;

function cleanup() {
  [].forEach.call(cards, function (card) {
    card.classList.remove('over');
  });
}

function handleDragStart(e) {
  dragSrcEl = this;
  console.log(this);
  this.style.opacity = '0.4';
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/html', this.innerHTML);
}

function handleDragOver(e) {
  if (e.preventDefault) {
    e.preventDefault();
  }

  e.dataTransfer.dropEffect = 'move';

  return false;
}

function handleDragEnter(e) {
  cleanup();
  dragging++;
  this.classList.add('over');
}

function handleDragLeave(e) {
  dragging--;
  if (dragging === 0) {
    this.classList.remove('over');
  }
}

function handleDrop(e) {
  if (e.stopPropagation) {
    e.stopPropagation();
  }

  if (!dragSrcEl) {
    cleanup();
    return false;
  }

  if (dragSrcEl != this) {
    dragSrcEl.innerHTML = this.innerHTML;
    this.innerHTML = e.dataTransfer.getData('text/html');
  }

  return false;
}

function handleDragEnd(e) {
  this.style.opacity = '1.0';
  cleanup();
  dragSrcEl = null;
  dragging = 0;
}

var cards = document.querySelectorAll('#project-cards .card');
[].forEach.call(cards, function(card) {
  card.addEventListener('dragstart', handleDragStart, false);
  card.addEventListener('dragenter', handleDragEnter, false);
  card.addEventListener('dragover', handleDragOver, false);
  card.addEventListener('dragleave', handleDragLeave, false);
  card.addEventListener('drop', handleDrop, false);
  card.addEventListener('dragend', handleDragEnd, false);
});