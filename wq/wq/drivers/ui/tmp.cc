

 public:
  

  
  #~PackageView() override;

  #void consoleAppend(char* text);

  #void open();
  #void save();

  #void dragEnterEvent(QDragEnterEvent *a_event) override;
  #void dragLeaveEvent(QDragLeaveEvent *a_event) override;
  #void dragMoveEvent(QDragMoveEvent *a_event) override;
  #void dropEvent(QDropEvent *a_event) override;
  #void keyPressEvent(QKeyEvent *a_event) override;
  #void keyReleaseEvent(QKeyEvent *a_event) override;
  #void wheelEvent(QWheelEvent *a_event) override;
  #void drawBackground(QPainter *painter, QRectF const &a_rect) override;

  #LinkItem *dragLink() const { return m_dragLink; }
  #void setDragLink(LinkItem *a_link) { m_dragLink = a_link; }
  #void acceptDragLink() { m_dragLink = nullptr; }
  #void cancelDragLink();

  Editor const *editor() const { return m_editor; }
  Editor *editor() { return m_editor; }
  Package const *package() const { return m_package; }
  Package const *graph() const { return m_package; }
  Package *package() { return m_package; }
  Package *graph() { return m_package; }

  bool canClose();
  void center();
  bool snapToGrid() const { return m_snapToGrid; }

  void setFilename(QString const a_filename) { m_filename = a_filename; }
  QString filename() const { return m_filename; }

  void showProperties();

  void deleteElement();

  void updateName(Node *const a_node);
  void selectItem(QModelIndex const &a_index);

  Nodes &nodes() { return m_nodes; }
  Nodes const &nodes() const { return m_nodes; }

  Node *getNode(size_t const a_id) const { return m_nodes[a_id]; }

  NodesListModel *model() const { return m_nodesModel; }
  QSortFilterProxyModel *proxyModel() const { return m_nodesProxyModel; }

  void setSelectedNode(Node *const a_node);

 signals:
  void requestOpenFile(QString const a_filename);

 private:
  void updateGrid(qreal const a_scale);

 private:
  Editor *const m_editor{};
  QListView *const m_elements{};
  QTableWidget *const m_properties{};
  NodesListModel *const m_nodesModel{};
  QSortFilterProxyModel *const m_nodesProxyModel{};
  Package *const m_package{};
  Nodes m_nodes{};
  QGraphicsScene *const m_scene{};
  QTimer m_timer{};
  Node *const m_inputs{};
  Node *const m_outputs{};
  nodes::Package *m_packageNode{};
  Node *m_dragNode{};
  Node *m_selectedNode{};
  LinkItem *m_dragLink{};
  int32_t m_scheduledScalings{};
  enum class GridDensity { eLarge, eSmall } m_gridDensity{};
  QString m_filename{};
  bool m_snapToGrid{};
  bool m_standalone{};