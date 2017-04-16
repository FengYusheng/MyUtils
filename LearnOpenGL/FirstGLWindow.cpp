#include <iostream>
#include <GL\glew.h>
#include <FirstGLWindow.h>


void FirstGLWindow::initializeGL()
{
	glewInit();

	GLfloat verdices[] = {
		+0.0f, +0.0f,
		-1.0f, +1.0f,
		+1.0f, +1.0f,
		-1.0f, -1.0f,
		+1.0f, -1.0f
	};

	/*Send datas from RAM to graphic card.*/
	GLuint myBufferID;
	glGenBuffers(1, &myBufferID);
	glBindBuffer(GL_ARRAY_BUFFER, myBufferID);
	glBufferData(GL_ARRAY_BUFFER, sizeof(verdices), verdices, GL_STATIC_DRAW);

	/*Enable pipeline.*/
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, 0);


	/*You can change the order of these indices to modify the triangles.*/
	GLushort indices[] = { 0, 1, 2, 0, 3, 4 };
	GLuint indicesBufferID;
	glGenBuffers(1, &indicesBufferID);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indicesBufferID);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
}

void FirstGLWindow::paintGL()
{
	glViewport(0, 0, width(), height());
	//glDrawArrays(GL_TRIANGLES, 0, 6);
	glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_SHORT, 0);
}


FirstGLWindow::FirstGLWindow()
{
}


FirstGLWindow::~FirstGLWindow()
{
}
