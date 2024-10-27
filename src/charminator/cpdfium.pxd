cdef extern from "fpdfview.h":
    ctypedef void* FPDF_DOCUMENT
    ctypedef const char* FPDF_STRING
    ctypedef const char* FPDF_BYTESTRING
    ctypedef void* FPDF_PAGE
    ctypedef void* FPDF_TEXTPAGE
    ctypedef void* FPDF_PAGEOBJECT
    ctypedef unsigned short FPDF_WCHAR
    ctypedef int FPDF_BOOL
    ctypedef void* FPDF_FONT

    ctypedef enum FPDF_RENDERER_TYPE:
        FPDF_RENDERERTYPE_AGG,
        FPDF_RENDERERTYPE_SKIA

    ctypedef struct FS_RECTF:
      float left
      float top
      float right
      float bottom

    ctypedef struct FS_MATRIX:
      float a
      float b
      float c
      float d
      float e
      float f

    ctypedef struct FPDF_LIBRARY_CONFIG:
        int version
        const char** m_pUserFontPaths;
        void* m_pIsolate
        unsigned int m_v8EmbedderSlot
        void* m_pPlatform
        FPDF_RENDERER_TYPE m_RendererType



    void FPDF_InitLibraryWithConfig(const FPDF_LIBRARY_CONFIG * config) nogil
    void FPDF_DestroyLibrary() nogil
    unsigned long FPDF_GetLastError() nogil
    FPDF_DOCUMENT FPDF_LoadDocument(FPDF_STRING file_path, FPDF_BYTESTRING password) nogil
    void FPDF_CloseDocument(FPDF_DOCUMENT document) nogil
    FPDF_PAGE FPDF_LoadPage(FPDF_DOCUMENT document, int page_index) nogil
    void FPDF_ClosePage(FPDF_PAGE page) nogil
    float FPDF_GetPageWidthF(FPDF_PAGE page) nogil
    float FPDF_GetPageHeightF(FPDF_PAGE page) nogil
    int FPDF_GetPageCount(FPDF_DOCUMENT document) nogil
    FPDF_BOOL FPDF_GetPageBoundingBox(FPDF_PAGE page, FS_RECTF * rect) nogil

cdef extern from "fpdf_text.h":
    FPDF_TEXTPAGE FPDFText_LoadPage(FPDF_PAGE page) nogil
    void FPDFText_ClosePage(FPDF_TEXTPAGE text_page) nogil
    int FPDFText_CountChars(FPDF_TEXTPAGE text_page) nogil
    unsigned int FPDFText_GetUnicode(FPDF_TEXTPAGE text_page, int index) nogil
    FPDF_PAGEOBJECT FPDFText_GetTextObject(FPDF_TEXTPAGE text_page, int index) nogil
    int FPDFText_IsGenerated(FPDF_TEXTPAGE text_page, int index) nogil
    int FPDFText_IsHyphen(FPDF_TEXTPAGE text_page, int index) nogil
    int FPDFText_HasUnicodeMapError(FPDF_TEXTPAGE text_page, int index) nogil
    FPDF_BOOL FPDFText_GetCharBox(FPDF_TEXTPAGE text_page, int index, double * left, double * right, double * bottom, double * top) nogil
    FPDF_BOOL FPDFText_GetLooseCharBox(FPDF_TEXTPAGE text_page, int index, FS_RECTF * rect) nogil


cdef extern from "fpdf_edit.h":
    int FPDFPage_CountObjects(FPDF_PAGE page) nogil
    FPDF_PAGEOBJECT FPDFPage_GetObject(FPDF_PAGE page, int index) nogil
    int FPDFPageObj_GetType(FPDF_PAGEOBJECT page_object) nogil
    unsigned long FPDFTextObj_GetText(FPDF_PAGEOBJECT text_object,
                        FPDF_TEXTPAGE text_page,
                        FPDF_WCHAR* buffer,
                        unsigned long length) nogil
    FPDF_BOOL FPDFPageObj_GetBounds(FPDF_PAGEOBJECT page_object,
                          float * left,
                          float * bottom,
                          float * right,
                          float * top) nogil
    FPDF_FONT FPDFTextObj_GetFont(FPDF_PAGEOBJECT text) nogil
    FPDF_BOOL FPDFPageObj_HasTransparency(FPDF_PAGEOBJECT page_object) nogil
    FPDF_BOOL FPDFPageObj_GetMatrix(FPDF_PAGEOBJECT page_object, FS_MATRIX* matrix) nogil
    FPDF_BOOL FPDFTextObj_GetFontSize(FPDF_PAGEOBJECT text, float * size) nogil
    FPDF_BOOL FPDFPageObj_GetFillColor(FPDF_PAGEOBJECT page_object, unsigned int* R, unsigned int* G, unsigned int* B, unsigned int* A) nogil

    size_t FPDFFont_GetBaseFontName(FPDF_FONT font, char * buffer, size_t length) nogil
    size_t FPDFFont_GetFamilyName(FPDF_FONT font, char * buffer, size_t length) nogil
    int FPDFFont_GetFlags(FPDF_FONT font) nogil
    int FPDFFont_GetWeight(FPDF_FONT font) nogil
    FPDF_BOOL FPDFFont_GetItalicAngle(FPDF_FONT font, int* angle) nogil
