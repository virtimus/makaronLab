wx.App      -> QtApplication      -> wq.App
wx.Frame    -> QtMainWindow       -> wq.MainWindow/wq.Frame
wx.Control  -> QtWidget           -> wq.Element
wx.Panel    -> QMdiArea           -> wq.Panel
wx.BoxSizer -> QtLayout           -> wq.Layout
            -> QTTabWidget          ->wq.TabPanel
            ->QtWidget              ->wq.Tab