#ifndef FIRST_GL_WINDOW
#define FIRST_GL_WINDOW

#include <QtWidgets\qopenglwidget.h>

class FirstGLWindow : public QOpenGLWidget//public, private inherit?
{
protected:
	void initializeGL();
	void paintGL();
public:
	FirstGLWindow();
	~FirstGLWindow();
};


#endif
