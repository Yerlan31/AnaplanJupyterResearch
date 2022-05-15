# AnaplanJupyterResearch
Научно-исследовательская работа 6 семестра Кафедры "Автоматизированные системы обработки информации и  управления" МГТУ им. Баумана. "
<h2>Prerequisites:</h2>
<ul>
  <li> Run jupyter notebook
    
    jupyter notebook
    
   <li> Set endpoints on every cell needed to run (including #)
     
     # GET /run1
    
  <li> Run jupyter kernel for http requests 
    
    jupyter kernelgateway --KernelGatewayApp.api=kernel_gateway.notebook_http --KernelGatewayApp.seed_uri=./<notebook name>.ipynb --port=<any free port>
</ul>
