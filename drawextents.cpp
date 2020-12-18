/* PDF Output Routines */
/* Copyright 2017  Tailor Made Software */

#include "stdafx.h"
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>
#include <list>
#include <algorithm>
#include "math.h"
#include "filetype.hpp"
#include "gentypes.h"
#include "gentypes2.hpp"
#include "sfile.hpp"
#include "cverr.hpp"
#ifndef LINUX
#include <codecvt>
#endif

#ifdef RASTER
	#if defined(RASTER_FREE_IMAGE) && defined(FREEIMAGE_LIB)
		#include "FreeImage.h"
	#endif
#endif

#include "DbBlockTable.h"
#include "DbBlockTableRecord.h"
#include "DbBlockReference.h"
#include "DbDimension.h"
#include "DbCircle.h"
#include "DbPolyline.h"
#include "Db2dPolyline.h"
#include "Db3dPolyline.h"
#include "DbMText.h"
#include "DbText.h"

#include "OdString.h"
#include <sstream>

#include "CommonRoutines.hpp"
#include "ShowTrace.hpp"
#include "ShowTraceOD.hpp"
#include "formats.hpp"

#include "drawextents.hpp"

using namespace std;

#define MMTOINCH 2.83464567
#define LWFACTOR 1.44

extern OdString sExePath;
extern double polyFactor;
extern vector<double> LayoutScale;

extern OdDbDatabasePtr	pDwgDb;

#ifndef _WIN32
	#include <stdio.h>
	#include <unistd.h>
	#define _strlwr strlwr
	#define _strupr strupr
	#define _unlink unlink
#endif

#define DOPOLY 1
#define DOLINES 1
#define DOARCS 1
#define DOELLPS 1
#define DOTEXT 1
#define DOFILLS 1
#define DOPDFIMAGES 1
#define DOCLIP 1

DRAWEXTENTS::DRAWEXTENTS() : TRANS_BASE2()
{
//	currentFont = NULL;
	SetDoBlocks(false);
	BaseFileName.empty();
	ImageNumber = 0;
	SetDrawingWidth(2500);
	SetDrawingHeight(2500);
	Scale = 1.;
	MinLineWeight = 0.;
    ResetFile();
	FillColor = 0;
	BuildingName.empty();
	FloorName.empty();
	DrawingSheetCount = 0;
	ViewCount = 0;
	LayoutCount = 0;
	LayerNameList.clear();
	PageSizeSet = false;
}

DRAWEXTENTS::~DRAWEXTENTS()
{
}

int DRAWEXTENTS::GetFormat()
{
	return FMT_EXTENTS;
}

#ifdef DO_SNAPPOINTS
bool DRAWEXTENTS::AddSnapPoint(double x, double y)
{
	return false;
}
#endif

int DRAWEXTENTS::SetColorRGB(short red, short green, short blue)
{
	return 0;
}

bool DRAWEXTENTS::BeginGroup(OdString GroupName)
{
	try
		{

		}
	catch (...)
		{
		ShowError("Error in BeginGroup", GroupName);
		}

	return FALSE;
}

bool DRAWEXTENTS::EndGroup(OdString GroupName)
{
	try
		{
		}
	catch (...)
		{
		ShowError("Error in EndGroup", GroupName);
		}
	return FALSE;
}

bool DRAWEXTENTS::SetHyperlink(char *hyperlink, char *comment, int type)
{
	try
		{
		}
	catch (...)
		{
		ShowError("Error in SetHyperlink");
		}

	return FALSE;
}

bool DRAWEXTENTS::ClearHyperlink()
{
	CurrentURL = NULL;

	return FALSE;
}

void DRAWEXTENTS::MapLineStyle(OdString lineStyleName, double lss)
{
	return;
}

bool DRAWEXTENTS::GetLineStyleDef(OdString lineStyleName, double lss, vector<double> &dash_pattern)
{
	return true;
}



short DRAWEXTENTS::SetIslandCount(int Count)
{
	return FALSE;
}

short DRAWEXTENTS::SetIslandSize(int Size)
{
	return FALSE;
}

bool DRAWEXTENTS::IsRaster()
{
	return false;
}

bool DRAWEXTENTS::AllowTrueColors()
{
	return true;
}

bool DRAWEXTENTS::UseSingleFile()
{
	return true;
}

bool DRAWEXTENTS::HasLayers()
{
	return false;
}

bool DRAWEXTENTS::HasVisibility()
{
	return true;
}

void DRAWEXTENTS::OutputHtml()
{
}

double DRAWEXTENTS::LineWidthFactor()
{
	return GetLineWidthScaleFactor();
}

short DRAWEXTENTS::ResetFile()
{
	try
		{
		ShowTrace("In ResetFile EXTENTS");
		Epsilon = 1./pow(10.,tmsPrecision);

		PointCount = 0;
		LinePos = 0;
		ClipCount = 0;
		groupPos = 0;

		bInUrl = FALSE;
		SetLayerName("0");
//		SetPenWidth(0);
		SetColor(7);
		SetBackground(255);

		lastPenWidth = -1.;
		ProspectiveColor = -1;
		LayerNumber = -1;

		ViewNum = 0;
		LastCellHeight = 1.0;
		bColorSafe = FALSE;
		CurrentColor = -1;
		LastLineStyle = "";

		LastGroupName.empty();
		LastJsLayerName.empty();
		NodeLayerName.empty();
		bNodeLayer = false;

		URLs.clear();
		CurrentURL = NULL;
		CurrentFont = NULL;
		bFirstCheck = true;

		plines = NULL;
		lines = NULL;
		arcs = NULL;
		fills = NULL;
		ellp_circles = NULL;
		fonts = NULL;
		ShowTrace("Exit ResetFile Extents");
	}
	catch (...)
		{
		ShowError("Error in Extents ResetFile");
		}

	return(0);
}

short DRAWEXTENTS::NewPicture()
{
	return 0;
}

short DRAWEXTENTS::NewView(OdString viewName, long lx, long ly, long ux, long uy)
{
	*outstream << "ViewName: " << convertToUTF8(viewName) << endl;
	return (0);
}

int DRAWEXTENTS::DefineColor(short ColorNumber, short r, short b, short g)
{
	return FALSE;
}

bool DRAWEXTENTS::SetTint(double Tint)
{
	return FALSE;
}

double DRAWEXTENTS::CalculateLineWidth(double inWidth, int spaceType, bool bPolyType)
{
	return 0;
}

bool DRAWEXTENTS::FixOutputName(OdString &origOutputName)
{
	SetBaseFileName(origOutputName);
	origOutputName += L".extents";

	return false;
}

bool DRAWEXTENTS::CreateDrawing()
{
	if (OpenFile((wchar_t*)OutputFile.c_str(), FALSE, TRUE) < 0)
	{
#ifndef CVENT
		cout << "Output File Open Error" << endl << "File May Be In Use By Another Program" << endl;
#endif
		//		ErrorCode = errOutputFileOpen;
		return TRUE;
	}

	Header();
	return false;
}

bool DRAWEXTENTS::SaveDrawing()
{
	return false;
}

string FixTextString(OdString str)
{
	string contents = convertToUTF8(str);
	if (contents.size())
	{
#ifdef _DEBUG
		if (contents.size() > 100)
			int abc = 1;
#endif
		replaceAll(contents, "\t", "&#x9;");
		replaceAll(contents, "\n", "\\P");
		replaceAll(contents, "\\n", "\\P");
		replaceAll(contents, "\0A\0D", "\\P");
		replaceAll(contents, "\\", "\\\\");
		replaceAll(contents, "\\\\\\\\", "\\\\");
		if (contents.back() == '}')
			contents.pop_back();
		if (contents.front() == '{')
			contents = contents.substr(1);
	}
	return contents;
}

void  DRAWEXTENTS::DrawLine(FIBITMAP* bitmap, RGBQUAD* color, unsigned x1, unsigned y1, unsigned x2, unsigned y2)
{
	int dx = x2 - x1,
		dy = y2 - y1;
	bool bDraw = true;

	if (dx || dy) {
		if (abs(dx) >= abs(dy)) {
			float y = y1 + 0.5;
			float dly = float(dy) / float(dx);
			if (dx > 0)
				for (int x = x1; x <= x2; x++) {
					if (bDraw)
						FreeImage_SetPixelColor(bitmap, x, unsigned(floor(y)), color);
					bDraw = !bDraw;
					y += dly;
				}
			else
				for (int x = x1; x >= int(x2); x--) {
					if (bDraw)
						FreeImage_SetPixelColor(bitmap, x, unsigned(floor(y)), color);
					bDraw = !bDraw;
					y -= dly;
				}
		}
		else {
			float x = x1 + 0.5;
			float dlx = float(dx) / float(dy);
			if (dy > 0)
				for (int y = y1; y <= y2; y++) {
					if (bDraw)
						FreeImage_SetPixelColor(bitmap, unsigned(floor(x)), y, color);
					bDraw = !bDraw;
					x += dlx;
				}
			else
				for (int y = y1; y >= int(y2); y--) {
					if (bDraw)
						FreeImage_SetPixelColor(bitmap, unsigned(floor(x)), y, color);
					bDraw = !bDraw;
					x -= dlx;
				}
		}
	}
}

void DRAWEXTENTS::DrawRectangle(FIBITMAP* bitmap, RGBQUAD* color, unsigned minx, unsigned miny, unsigned maxx, unsigned maxy)
{
	unsigned x = minx;
	unsigned y;
	bool bDraw = true;
	for (y = miny; y <= maxy; y++)
	{
		if (bDraw)
			FreeImage_SetPixelColor(bitmap, x, y, color);
		bDraw = !bDraw;
	}
	x = maxx;
	for (y = miny; y <= maxy; y++)
	{
		if (bDraw)
			FreeImage_SetPixelColor(bitmap, x, y, color);
		bDraw = !bDraw;
	}
	y = miny;
	for (x = minx; x <= maxx; x++)
	{
		if (bDraw)
			FreeImage_SetPixelColor(bitmap, x, y, color);
		bDraw = !bDraw;
	}
	y = maxy;
	for (x = minx; x <= maxx; x++)
	{
		if (bDraw)
			FreeImage_SetPixelColor(bitmap, x, y, color);
		bDraw = !bDraw;
	}
	return;
}

void DRAWEXTENTS::ProcessText(tmsView theView, OdGePoint3d UCSOrg, OdDbMTextPtr pMText, double rasterScale, double rasterDY, FIBITMAP* sourceBitmap)
{
	cout << "ProcessMText" << endl;
	string contents = FixTextString(pMText->contents());
	*outstream << "    \"Contents\": \"" << contents << "\"," << endl;

	OdGeExtents3d ext;
	pMText->getGeomExtents(ext);
	double MinX = ext.minPoint().x;
	double MinY = ext.minPoint().y;
	double MaxX = ext.maxPoint().x;
	double MaxY = ext.maxPoint().y;
	OdGePoint3dArray boundingPoints;
	pMText->getBoundingPoints(boundingPoints);
	if (boundingPoints.size() > 1)
	{
		OdGeExtents3d extBP;
		extBP.set(boundingPoints[0], boundingPoints[1]);
		for (int iBP = 2; iBP < boundingPoints.size(); iBP++)
			extBP.addPoint(boundingPoints[iBP]);
		MinX = extBP.minPoint().x;
		MinY = extBP.minPoint().y;
		MaxX = extBP.maxPoint().x;
		MaxY = extBP.maxPoint().y;
	}

	double rasMinX = (MinX - theView.DWGExtents.MinX) * rasterScale;
	double rasMinY = (long)(rasterDY + 0.99) - (long)((MinY - theView.DWGExtents.MinY) * rasterScale);
	double rasMaxX = (MaxX - theView.DWGExtents.MinX) * rasterScale;
	double rasMaxY = (long)(rasterDY + 0.99) - (long)((MaxY - theView.DWGExtents.MinY) * rasterScale);

	*outstream << "    \"Entity_Extents\": {" << endl;
	*outstream << "        \"Minimum_Point\": {" << endl;
	*outstream << "            \"x\": " << ext.minPoint().x + UCSOrg.x << "," << endl;
	*outstream << "            \"y\": " << ext.minPoint().y + UCSOrg.y << "," << endl;
	*outstream << "            \"z\": " << ext.minPoint().z + UCSOrg.z << endl;
	*outstream << "            }," << endl;
	*outstream << "        \"Maximum_Point\": {" << endl;
	*outstream << "            \"x\": " << ext.maxPoint().x + UCSOrg.x << "," << endl;
	*outstream << "            \"y\": " << ext.maxPoint().y + UCSOrg.y << "," << endl;
	*outstream << "            \"z\": " << ext.maxPoint().z + UCSOrg.z << endl;
	*outstream << "            }," << endl;
	*outstream << "        \"Min_Raster_X\": \"" << (long)(rasMinX + 0.99) << "\"," << endl;
	*outstream << "        \"Min_Raster_Y\": \"" << (long)(rasMinY + 0.99) << "\"," << endl;
	*outstream << "        \"Max_Raster_X\": \"" << (long)(rasMaxX + 0.99) << "\"," << endl;
	*outstream << "        \"Max_Raster_Y\": \"" << (long)(rasMaxY + 0.99) << "\"" << endl;
	*outstream << "        }" << endl;

	RGBQUAD color;
	color.rgbRed = 200;
	color.rgbGreen = 50;
	color.rgbBlue = 50;
	color.rgbReserved = 255;
	DrawRectangle(sourceBitmap, &color, (long)(rasMinX + 0.99), (long)(rasterDY - rasMinY + 0.99), (long)(rasMaxX + 0.99), (long)(rasterDY - rasMaxY + 0.99));
}

void DRAWEXTENTS::ProcessCircle(tmsView theView, OdGePoint3d UCSOrg, OdDbCirclePtr pCircle, double rasterScale, double rasterDY, FIBITMAP* sourceBitmap)
{
	cout << "ProcessCircle" << endl;
	OdGePoint3d center;
	center = pCircle->center();
	*outstream << "    \"Center\": {" << endl;
	*outstream << "            \"x\": " << center.x + UCSOrg.x << "," << endl;
	*outstream << "            \"y\": " << center.y + UCSOrg.y << "," << endl;
	*outstream << "            \"z\": " << center.z + UCSOrg.z << endl;
	*outstream << "            }," << endl;
	*outstream << "    \"Radius\": \"" << pCircle->radius() << "\"," << endl;

	OdGeExtents3d ext;
	pCircle->getGeomExtents(ext);
	double MinX = ext.minPoint().x;
	double MinY = ext.minPoint().y;
	double MaxX = ext.maxPoint().x;
	double MaxY = ext.maxPoint().y;

	double rasMinX = (MinX - theView.DWGExtents.MinX) * rasterScale;
	double rasMinY = (long)(rasterDY + 0.99) - (long)((MinY - theView.DWGExtents.MinY) * rasterScale);
	double rasMaxX = (MaxX - theView.DWGExtents.MinX) * rasterScale;
	double rasMaxY = (long)(rasterDY + 0.99) - (long)((MaxY - theView.DWGExtents.MinY) * rasterScale);

	*outstream << "    \"Entity_Extents\": {" << endl;
	*outstream << "        \"Minimum_Point\": {" << endl;
	*outstream << "            \"x\": " << ext.minPoint().x + UCSOrg.x << "," << endl;
	*outstream << "            \"y\": " << ext.minPoint().y + UCSOrg.y << "," << endl;
	*outstream << "            \"z\": " << ext.minPoint().z + UCSOrg.z << endl;
	*outstream << "            }," << endl;
	*outstream << "        \"Maximum_Point\": {" << endl;
	*outstream << "            \"x\": " << ext.maxPoint().x + UCSOrg.x << "," << endl;
	*outstream << "            \"y\": " << ext.maxPoint().y + UCSOrg.y << "," << endl;
	*outstream << "            \"z\": " << ext.maxPoint().z + UCSOrg.z << endl;
	*outstream << "            }," << endl;
	*outstream << "        \"Min_Raster_X\": \"" << (long)(rasMinX + 0.99) << "\"," << endl;
	*outstream << "        \"Min_Raster_Y\": \"" << (long)(rasMinY + 0.99) << "\"," << endl;
	*outstream << "        \"Max_Raster_X\": \"" << (long)(rasMaxX + 0.99) << "\"," << endl;
	*outstream << "        \"Max_Raster_Y\": \"" << (long)(rasMaxY + 0.99) << "\"" << endl;
	*outstream << "        }" << endl;

	RGBQUAD color;
	color.rgbRed = 50;
	color.rgbGreen = 200;
	color.rgbBlue = 50;
	color.rgbReserved = 255;
	DrawRectangle(sourceBitmap, &color, (long)(rasMinX + 0.99), (long)(rasterDY - rasMinY + 0.99), (long)(rasMaxX + 0.99), (long)(rasterDY - rasMaxY + 0.99));
}

void DRAWEXTENTS::ProcessInsert(tmsView theView, OdGePoint3d UCSOrg, OdDbBlockReferencePtr pInsert, double rasterScale, double rasterDY, FIBITMAP* sourceBitmap)
{
	cout << "ProcessInsert" << endl;

	OdGeExtents3d ext;
	pInsert->getGeomExtents(ext);
	double MinX = ext.minPoint().x;
	double MinY = ext.minPoint().y;
	double MaxX = ext.maxPoint().x;
	double MaxY = ext.maxPoint().y;

	double rasMinX = (MinX - theView.DWGExtents.MinX) * rasterScale;
	double rasMinY = (long)(rasterDY + 0.99) - (long)((MinY - theView.DWGExtents.MinY) * rasterScale);
	double rasMaxX = (MaxX - theView.DWGExtents.MinX) * rasterScale;
	double rasMaxY = (long)(rasterDY + 0.99) - (long)((MaxY - theView.DWGExtents.MinY) * rasterScale);

	*outstream << "    \"Entity_Extents\": {" << endl;
	*outstream << "        \"Minimum_Point\": {" << endl;
	*outstream << "            \"x\": " << ext.minPoint().x + UCSOrg.x << "," << endl;
	*outstream << "            \"y\": " << ext.minPoint().y + UCSOrg.y << "," << endl;
	*outstream << "            \"z\": " << ext.minPoint().z + UCSOrg.z << endl;
	*outstream << "            }," << endl;
	*outstream << "        \"Maximum_Point\": {" << endl;
	*outstream << "            \"x\": " << ext.maxPoint().x + UCSOrg.x << "," << endl;
	*outstream << "            \"y\": " << ext.maxPoint().y + UCSOrg.y << "," << endl;
	*outstream << "            \"z\": " << ext.maxPoint().z + UCSOrg.z << endl;
	*outstream << "            }," << endl;
	*outstream << "        \"Min_Raster_X\": \"" << (long)(rasMinX + 0.99) << "\"," << endl;
	*outstream << "        \"Min_Raster_Y\": \"" << (long)(rasMinY + 0.99) << "\"," << endl;
	*outstream << "        \"Max_Raster_X\": \"" << (long)(rasMaxX + 0.99) << "\"," << endl;
	*outstream << "        \"Max_Raster_Y\": \"" << (long)(rasMaxY + 0.99) << "\"" << endl;
	*outstream << "        }" << endl;

	RGBQUAD color;
	color.rgbRed = 50;
	color.rgbGreen = 50;
	color.rgbBlue = 200;
	color.rgbReserved = 255;
	DrawRectangle(sourceBitmap, &color, (long)(rasMinX + 0.99), (long)(rasterDY - rasMinY + 0.99), (long)(rasMaxX + 0.99), (long)(rasterDY - rasMaxY + 0.99));
}

void DRAWEXTENTS::ProcessPolyline(tmsView theView, OdGePoint3d UCSOrg, OdDbEntityPtr ptrEntity, double rasterScale, double rasterDY, FIBITMAP* sourceBitmap)
{
	OdGePoint3d pt;
	OdGePoint3dArray pts;
	pts.clear();
	cout << "ProcessPolyline" << endl;

	if (ptrEntity->isA() == OdDbPolyline::desc())
	{
		cout << "Polyline" << endl;
		OdDbPolylinePtr pPolyline = (OdDbPolylinePtr)ptrEntity;
		for (int i = 0; i < (int)pPolyline->numVerts(); i++)
		{
			pPolyline->getPointAt(i, pt);
			pts.append(pt);
		}
		if (pPolyline->isClosed())
		{
			pPolyline->getPointAt(0, pt);
			pts.append(pt);
		}
	}
	else if (ptrEntity->isA() == OdDb2dPolyline::desc())
	{
		cout << "2d Polyline" << endl;
		OdDb2dPolylinePtr pPolyline = (OdDb2dPolylinePtr)ptrEntity;
		OdDb2dVertex pVertex;
		OdDbObjectIteratorPtr pVertIt;
		pVertIt = pPolyline->vertexIterator();
		int vertexCount = 0;
		OdGePoint3d pt0;
		for (pVertIt->start(); !pVertIt->done(); pVertIt->step())
		{
			OdDbObjectId obj = pVertIt->entity()->objectId();
			OdDb2dVertexPtr pVertex = (OdDb2dVertexPtr)obj.safeOpenObject();
			pt = pPolyline->vertexPosition(*pVertex);
			pts.append(pt);
			if (vertexCount++ == 0)
				pt0 = pt;
		}
		if ((pPolyline->isClosed()) && (vertexCount > 0))
			pts.append(pt0);
	}
	else if (ptrEntity->isA() == OdDb3dPolyline::desc())
		cout << "3d Polyline" << endl;


	OdGeExtents3d ext;
	ptrEntity->getGeomExtents(ext);
	double MinX = ext.minPoint().x;
	double MinY = ext.minPoint().y;
	double MaxX = ext.maxPoint().x;
	double MaxY = ext.maxPoint().y;

	double rasMinX = (MinX - theView.DWGExtents.MinX) * rasterScale;
	double rasMinY = (long)(rasterDY + 0.99) - (long)((MinY - theView.DWGExtents.MinY) * rasterScale);
	double rasMaxX = (MaxX - theView.DWGExtents.MinX) * rasterScale;
	double rasMaxY = (long)(rasterDY + 0.99) - (long)((MaxY - theView.DWGExtents.MinY) * rasterScale);

	*outstream << "    \"Entity_Extents\": {" << endl;
	*outstream << "        \"Minimum_Point\": {" << endl;
	*outstream << "            \"x\": " << ext.minPoint().x + UCSOrg.x << "," << endl;
	*outstream << "            \"y\": " << ext.minPoint().y + UCSOrg.y << "," << endl;
	*outstream << "            \"z\": " << ext.minPoint().z + UCSOrg.z << endl;
	*outstream << "            }," << endl;
	*outstream << "        \"Maximum_Point\": {" << endl;
	*outstream << "            \"x\": " << ext.maxPoint().x + UCSOrg.x << "," << endl;
	*outstream << "            \"y\": " << ext.maxPoint().y + UCSOrg.y << "," << endl;
	*outstream << "            \"z\": " << ext.maxPoint().z + UCSOrg.z << endl;
	*outstream << "            }," << endl;
	*outstream << "        \"Min_Raster_X\": \"" << (long)(rasMinX + 0.99) << "\"," << endl;
	*outstream << "        \"Min_Raster_Y\": \"" << (long)(rasMinY + 0.99) << "\"," << endl;
	*outstream << "        \"Max_Raster_X\": \"" << (long)(rasMaxX + 0.99) << "\"," << endl;
	*outstream << "        \"Max_Raster_Y\": \"" << (long)(rasMaxY + 0.99) << "\"" << endl;
	*outstream << "        }";

	RGBQUAD color;
	color.rgbRed = 255;
	color.rgbGreen = 0;
	color.rgbBlue = 0;
	color.rgbReserved = 255;

	if (pts.size() >= 2)
	{
		*outstream << "," << endl << "    \"Raster_Vertices\": [" << endl;
		double x1 = (pts[0].x - theView.DWGExtents.MinX) * rasterScale;
		double y1 = (pts[0].y - theView.DWGExtents.MinY) * rasterScale;

		long lx1 = (long)(x1 + 0.49);
		long ly1 = (long)(y1 + 0.49);
		*outstream << "        {" << endl << "        \"x\": \"" << lx1 << "\"," << endl;
		*outstream << "        \"y\": \"" << ly1 << "\"" << endl;
		*outstream << "        }," << endl;

		for (int i = 1; i < pts.size(); i++)
		{
			double x2 = (pts[i].x - theView.DWGExtents.MinX) * rasterScale;
			double y2 = (pts[i].y - theView.DWGExtents.MinY) * rasterScale;
			long lx2 = (long)(x2 + 0.49);
			long ly2 = (long)(y2 + 0.49);
			DrawLine(sourceBitmap, &color, lx1, ly1, lx2, ly2);
			*outstream << "        {" << endl << "        \"x\": \"" << lx2 << "\"," << endl;
			*outstream << "        \"y\": \"" << ly2 << "\"" << endl;
			if (i != (pts.size()-1))
				*outstream << "        }," << endl;
			else
				*outstream << "        }" << endl;
			lx1 = lx2;
			ly1 = ly2;
		}
		*outstream << "    ]" << endl;
	}
	else
		*outstream << endl;
}

bool DRAWEXTENTS::OutputDrawing(bool bFirstDrawing)
{
	FIBITMAP* sourceBitmap;
	string outfile;
	bool bDoRasterManipulation = false;
	OdGePoint3d UCSOrg = pDwgDb->getUCSORG();
	*outstream << "\"Views\":" << endl << "  [ " << endl;
	for (std::vector<tmsView>::iterator viewIt = theDrawing.views.begin(); viewIt != theDrawing.views.end(); ++viewIt)
	{
		cout << "Set View" << endl;
		tmsView theView = (*viewIt);
		if (viewIt == theDrawing.views.begin())
			*outstream << "    { " << endl;
		else
			*outstream << "," << endl << "    { " << endl;
		OdAnsiString vName;
		vName = theView.ViewName;
		cout << "Output View" << endl;
		*outstream << "    \"View_Name\": \"" << vName.c_str() << "\"," << endl;

		OdGePoint3d UCSOrg;
		if (!vName.iCompare("ModelSpace"))
			UCSOrg = -1 * pDwgDb->getUCSORG();
		else
			UCSOrg = OdGePoint3d(0., 0., 0.);

		double dwgDX = theView.DWGExtents.MaxX - theView.DWGExtents.MinX;
		double dwgDY = theView.DWGExtents.MaxY - theView.DWGExtents.MinY;

		*outstream << "    \"DWG_Min_Point\": {" << endl;
		*outstream << "       \"x\": \"" << theView.DWGExtents.MinX + UCSOrg.x << "\"," << endl;
		*outstream << "       \"y\": \"" << theView.DWGExtents.MinY + UCSOrg.y << "\"" << endl << "        }," << endl;
		*outstream << "    \"DWG_Max_Point\": {" << endl;
		*outstream << "       \"x\": \"" << theView.DWGExtents.MaxX + UCSOrg.x << "\"," << endl;
		*outstream << "       \"y\": \"" << theView.DWGExtents.MaxY + UCSOrg.y << "\"" << endl << "        }," << endl;

//		double rasterDX = theView.Extents.MaxX - theView.Extents.MinX;
//		double rasterDY = theView.Extents.MaxY - theView.Extents.MinY;
		double rasterDX, rasterDY;
		if (!GetPageSize(rasterDX, rasterDY))
		{
			rasterDX = GetWidth();
			rasterDY = GetHeight();
		}

		*outstream << "    \"Raster_Width\": \"" << (long)(rasterDX + 0.99) << "\"," << endl;
		*outstream << "    \"Raster_Height\": \"" << (long)(rasterDY + 0.99) << "\"," << endl;

		*outstream << "    \"Scale_X\": \"" << (rasterDX/dwgDX) << "\"," << endl;
		*outstream << "    \"Scale_Y\": \"" << (rasterDY/dwgDY) << "\"";
		double rasterScale = MIN(rasterDX / dwgDX, rasterDY / dwgDY);

		if (!vName.iCompare("ModelSpace"))
		{
			outfile = convertToUTF8(GetOutputFile());
			replaceAll(outfile, ".extents", ".png");
			if ((fileExists(outfile)) && (!bDoRasterManipulation))
			{
				FreeImage_Initialise();
				sourceBitmap = FreeImage_Load(FIF_PNG, outfile.c_str());

				/* check that the image was properly loaded */
				if (!sourceBitmap) {
					ShowError("Could not load Image File", outfile);

					/* Unload the FreeImage library */
					FreeImage_DeInitialise();
				}
				else
					bDoRasterManipulation = true;
			}

			OdDbBlockTableRecordPtr pModelSpaceBlock = pDwgDb->getModelSpaceId().safeOpenObject(OdDb::kForWrite);
			*outstream << "," << endl << "\"Texts\":" << endl << "  [ " << endl;

			OdDbObjectIteratorPtr pEntIter = pModelSpaceBlock->newIterator(true, true, false);
			bool bFirstItem = true;
			for (; !pEntIter->done(); pEntIter->step())
			{
				OdDbEntityPtr ptrEntity = pEntIter->objectId().safeOpenObject(OdDb::kForWrite);
				if (ptrEntity->isA() == OdDbMText::desc())
				{
					OdDbMTextPtr pMText = (OdDbMTextPtr)ptrEntity;
					if (bFirstItem)
						*outstream << "    { " << endl;
					else
						*outstream << "," << endl << "    { " << endl;
					bFirstItem = false;
					ProcessText(theView, UCSOrg, pMText, rasterScale, rasterDY, sourceBitmap);

					*outstream << "    }";
				}
			}
			*outstream << endl << "  ]," << endl << "\"Circles\":" << endl << "  [ " << endl;

			pEntIter = pModelSpaceBlock->newIterator(true, true, false);
			bFirstItem = true;
			for (; !pEntIter->done(); pEntIter->step())
			{
				OdDbEntityPtr ptrEntity = pEntIter->objectId().safeOpenObject(OdDb::kForWrite);
				if (ptrEntity->isA() == OdDbCircle::desc())
				{
					OdDbCirclePtr pCircle = (OdDbCirclePtr)ptrEntity;
					if (bFirstItem)
						*outstream << "    { " << endl;
					else
						*outstream << "," << endl << "    { " << endl;
					bFirstItem = false;
					ProcessCircle(theView, UCSOrg, pCircle, rasterScale, rasterDY, sourceBitmap);

					*outstream << "    }";
				}
			}
			*outstream << endl << "  ]," << endl << "\"BlockInserts\":" << endl << "  [ " << endl;

			pEntIter = pModelSpaceBlock->newIterator(true, true, false);
			bFirstItem = true;
			for (; !pEntIter->done(); pEntIter->step())
			{
				OdDbEntityPtr ptrEntity = pEntIter->objectId().safeOpenObject(OdDb::kForWrite);
				if (ptrEntity->isA() == OdDbBlockReference::desc())
				{
					OdDbBlockReferencePtr pInsert = (OdDbBlockReferencePtr)ptrEntity;
					if (bFirstItem)
						*outstream << "    { " << endl;
					else
						*outstream << "," << endl << "    { " << endl;
					bFirstItem = false;
					ProcessInsert(theView, UCSOrg, pInsert, rasterScale, rasterDY, sourceBitmap);

					*outstream << "    }";
				}
			}
			*outstream << endl << "  ]," << endl << "\"Polylines\":" << endl << "  [ " << endl;

			pEntIter = pModelSpaceBlock->newIterator(true, true, false);
			bFirstItem = true;
			for (; !pEntIter->done(); pEntIter->step())
			{
				OdDbEntityPtr ptrEntity = pEntIter->objectId().safeOpenObject(OdDb::kForWrite);
				if ((ptrEntity->isA() == OdDbPolyline::desc()) || (ptrEntity->isA() == OdDb2dPolyline::desc()) || (ptrEntity->isA() == OdDb3dPolyline::desc()))
				{
					if (ptrEntity->isA() == OdDbPolyline::desc())
						cout << "Polyline" << endl;
					else if (ptrEntity->isA() == OdDb2dPolyline::desc())
						cout << "2d Polyline" << endl;
					else if (ptrEntity->isA() == OdDb3dPolyline::desc())
						cout << "3d Polyline" << endl;
					//OdDbPolylinePtr pPoly = (OdDbPolylinePtr)ptrEntity;
					if (bFirstItem)
						*outstream << "    { " << endl;
					else
						*outstream << "," << endl << "    { " << endl;
					bFirstItem = false;
					ProcessPolyline(theView, UCSOrg, ptrEntity, rasterScale, rasterDY, sourceBitmap);

					*outstream << "    }";
				}
			}
			*outstream << endl << "  ] " << endl;
		}
		else
			*outstream << endl;

		*outstream << "    } ";
	}
	*outstream << endl << "  ] " << endl;
	*outstream << "} " << endl;

	if (bDoRasterManipulation)
	{
		string newFile = outfile;
		replaceAll(newFile, ".png", "_new.png");
		FreeImage_Save(FIF_PNG, sourceBitmap, newFile.c_str(), 0);

		/* Release the image data structure */
		FreeImage_Unload(sourceBitmap);
		FreeImage_DeInitialise();
	}

	return false;
}

short DRAWEXTENTS::Header()
{
	ShowTrace("Create File Header");
	outstream = GetStream();

	*outstream << "{" << endl;
	return false;
}

short DRAWEXTENTS::DefineFont(OdString fontName)
{
	return true;
}

short DRAWEXTENTS::StandardizeLayerNames()
{
	for (std::list<tmsLayer>::iterator it = CurrentView->Layers.begin(); it != CurrentView->Layers.end(); ++it)
		{
		OdString ModLayerName = trim((*it).LayerName);
//		ModLayerName.makeUpper();
		std::string lName = OdAnsiString(ModLayerName).c_str();
		(*it).sLayerName = lName;

		ModLayerName.replace(L"\\U+", L"\\u");

		int found = ModLayerName.findOneOf(L" #&()-.$[]|?@!%^*{}");
		while (found!=-1)
			{
			ModLayerName.setAt(found, '_');
			found=ModLayerName.findOneOf(L" #&()-.$[]|?@!%^*{}");
			}

		char unicode_subs[64] = {'A','A','A','A','A','A','_','C','E','E','E','E','I','I','I','I','D','N','O','O','O','O','O','x',
				'O','U','U','U','U','Y','P','_','a','a','a','a','a','a','_','c','e','e','e','e','i','i','i','i','o','n','o','o',
				'o','o','o','_','0','u','u','u','u','y','p','y'};

		OdString tmp;
		tmp = L"  ";
		tmp.setAt(0, (unsigned int)198);
		tmp.setAt(1, '\0');
		ModLayerName.replace(tmp , "AE");

		tmp.setAt(0, (unsigned int)223);
		ModLayerName.replace(tmp, "SS");

		tmp.setAt(0, (unsigned int)230);
		ModLayerName.replace(tmp, "ae");

		tmp.setAt(0, (unsigned int)216);
		ModLayerName.replace(tmp, "OE");

		tmp.setAt(0, (unsigned int)248);
		ModLayerName.replace(tmp, "oe");

		for (int i=0; i < (int)(ModLayerName.getLength()); i++)
			{
#ifdef LINUX
			uint8_t bch = ModLayerName[i];
#else
			short bch = OdAnsiString(ModLayerName).getAt(i);
#endif
			if ((bch >= (unsigned int)160) && (bch <= (unsigned int)192))
				ModLayerName.setAt(i, '_');
			else if ((bch >= (unsigned int)192) && (bch <= (unsigned int)255))
				ModLayerName.setAt(i, unicode_subs[bch-192]);
			}
		ModLayerName.replace(L"__", L"_");

		(*it).ModLayerName = ModLayerName;

		OdStringArray::size_type index=0;
		if (!LayerNameList.find(ModLayerName, index))
			LayerNameList.append(ModLayerName);
		}
	return false;
}

short DRAWEXTENTS::SetColorLW(unsigned int r, unsigned int g, unsigned int b, double lw)
{
	return false;
}

short DRAWEXTENTS::DefineLineWidth(double lw)
{
	return false;
}

short DRAWEXTENTS::OutputColor(int clr)
{
	return false;
}

short DRAWEXTENTS::OutputEntities()
{
	std::list<tmsGroup>::iterator itGrp;
	for (std::vector<tmsView>::iterator it = theDrawing.views.begin(); it != theDrawing.views.end(); ++it)
	{
		try {
		SetDrawingExtents(&(*it));
		if (EmptyDrawing(&(*it)))
			ShowError("Empty View, Ignored", (*it).ViewName);

		double hgt, wid;

		if (!GetPageSize(wid, hgt))
		{
			hgt = GetHeight();
			wid = GetWidth();
		}

	}
	catch (...) {
		cerr << "Generic C++ exception occurred!" << endl;
		return 99;
	}
}
	return false;
}

short DRAWEXTENTS::OutputLayers(std::list<tmsLayer>* layers, bool bDoFills)
{
	return false;
}

short DRAWEXTENTS::OutputLayerTable()
{

	return false;
}

short DRAWEXTENTS::Trailer()
{
	ShowTrace("  Close File");
	CloseFile();
	ShowTrace("  Garbage Collection");
	GarbageCollection();
	return(0);
}

short DRAWEXTENTS::OutputProperties()
{
    return(0);
}

bool DRAWEXTENTS::SupportsEllipse()
{
	return true;
}

bool DRAWEXTENTS::OutputFill(std::vector<tmsPolyline> fill)
{
	return false;
}

bool DRAWEXTENTS::OutputArcs(std::vector<tmsArc> arcs)
{
	return false;
}

void DRAWEXTENTS::CheckFont(std::string fontname)
{
}

bool DRAWEXTENTS::OutputFonts(std::vector<tmsFont> fonts)
{
	return false;
}

bool DRAWEXTENTS::CalculateColors(unsigned int r, unsigned int g, unsigned int b, unsigned int &grey)
{
return false;
}

bool DRAWEXTENTS::OutputText(std::vector<tmsText> texts, double fontSize)
{
	return false;
}

void DRAWEXTENTS::OutputURLExtents(OdGeExtents2d ext)
{
	return;
}

void DRAWEXTENTS::OutputURLPath(tmsURL url)
{
	return;
}

void DRAWEXTENTS::OutputNodePath(std::vector<tmsPolyline> path)
{
	return;
}

void DRAWEXTENTS::OutputURLs(bool bNodeFile)
{
	return;
}

void DRAWEXTENTS::OutputNodes(bool bNodeFile)
{
	return;
}

bool DRAWEXTENTS::OutputEllipsesAtSize(std::vector<tmsEllipse> &items, double lw)
{
	return false;
}

bool DRAWEXTENTS::OutputEllipses(std::vector<tmsEllipse> &items)
{
	return false;
}

bool DRAWEXTENTS::OutputEmbeddedImages(std::vector<tmsEmbeddedImage> &images)
{
	return false;
}

bool DRAWEXTENTS::OutputPath(std::vector<tmsPolyline> plines)
{
	return false;
}

bool DRAWEXTENTS::OutputLines(std::vector<tmsLine> lines)
{
	return false;
}

void DRAWEXTENTS::ProcessXData(OdResBufPtr resbuf)
{
	return;
}