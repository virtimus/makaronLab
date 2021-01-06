import sys
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QWidget, QStyle
from ui_editor import Ui_Editor
import consts

class Registry:
    def __init__(self, editor):
        #nop?
        print("dupa")
        
    @staticmethod    
    def instance(editor):
        return Registry(editor);

# file:///src/ews.i3c/makaronLab/externalTools/spaghetti/libspaghetti/source/ui/editor.cc
class Editor(QMainWindow):
    def __init__(self,parent):
        super(Editor, self).__init__(parent)
        self._ui = Ui_Editor()
        self._ui.setupUi(self)
        self._registry = Registry.instance(self);
        self.setObjectName(consts.HDUI_NAME);
        
        #clear stuff
        self._ui.elementsContainer.removeItem(0);
        self._ui.packagesContainer.removeItem(0);
        self._ui.tabWidget.removeTab(0);
        self._ui.clearSearchText.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        self._ui.elementsList.setIconSize(consts.HDUI_ICON_SIZE)
        self._ui.elementsList.setSpacing(5)
        self._ui.elementsList.setUniformItemSizes(True)
        '''TODO
  connect(m_ui->actionNew, &QAction::triggered, this, &Editor::newPackage);
  connect(m_ui->actionOpen, &QAction::triggered, this, &Editor::openPackage);
  connect(m_ui->actionReloadAll, &QAction::triggered, this, &Editor::reloadAll);
  connect(m_ui->actionSave, &QAction::triggered, this, &Editor::savePackage);
  connect(m_ui->actionSaveAs, &QAction::triggered, this, &Editor::saveAsPackage);
  connect(m_ui->actionClose, &QAction::triggered, this, &Editor::closePackage);
  connect(m_ui->actionCloseAll, &QAction::triggered, this, &Editor::closeAllPackages);

  connect(m_ui->actionDeleteElement, &QAction::triggered, this, &Editor::deleteElement);

  connect(m_ui->actionShowLibrary, &QAction::triggered, this, &Editor::showLibrary);
  connect(m_ui->actionShowProperties, &QAction::triggered, this, &Editor::showProperties);

  connect(m_ui->actionBuildCommit, &QAction::triggered, this, &Editor::buildCommit);
  connect(m_ui->actionRecentChanges, &QAction::triggered, this, &Editor::recentChanges);
  connect(m_ui->actionAbout, &QAction::triggered, this, &Editor::about);
  connect(m_ui->actionAboutQt, &QAction::triggered, this, &Editor::aboutQt);
  connect(m_ui->tabWidget, &QTabWidget::tabCloseRequested, this, &Editor::tabCloseRequested);
  connect(m_ui->tabWidget, &QTabWidget::currentChanged, this, &Editor::tabChanged);

  connect(m_ui->elementsList, &QListView::doubleClicked, [this](QModelIndex const &a_index) {
    (void)a_index;

    auto const view = packageView();
    if (!view) return;

    view->selectItem(a_index);
  });

  connect(m_ui->clearSearchText, &QToolButton::clicked, [this] { m_ui->searchNode->clear(); });

  connect(m_ui->searchNode, &QLineEdit::textChanged, [this](QString const &a_search) {
    m_ui->clearSearchText->setDisabled(a_search.isEmpty());

    auto const view = packageView();
    if (!view) return;

    auto const model = view->proxyModel();
    model->setFilterWildcard(a_search);
  });

  shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F), self)
  connect(shortcut, &QShortcut::activated, [this] { m_ui->searchNode->setFocus(); });
'''
        packagesDir = QDir(consts.HDUI_PACKAGES_DIR)
        if (not packagesDir.exists()):
            packagesDir.mkpath(".")  
  
''' Main App Entry
'''  
  
app = QApplication(sys.argv)
window = QMainWindow()
editor = Editor(None);
editor.show()
sys.exit(app.exec_())    
