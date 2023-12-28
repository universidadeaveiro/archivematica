# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   30-05-2022 22:14:39
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 30-05-2022 22:21:59
# @Description: 
import textwrap

OK_TEXT = textwrap.dedent(f"""\
    Ex.mo(a) Senhor(a), 
        
    O arquivo que tentou obter através do Archivematica não está imediatamente disponível.
    Estamos, neste momento, a trabalhar para recuperar o mesmo, sendo que nas próximas 24h deverá receber um e-mail a notificá-lo de que o arquivo está disponível para download. 
    
    Após receber o e-mail de notificação, o arquivo ficará disponível por um curto período de dias.
    Posteriormente, o mesmo será movido para arquivo profundo.
    
    Obrigado,
    Arquivo Geral da Universidade de Aveiro

    -----------------------------

    Hello, 

    ....
    < mensagem em ingles aqui>
    """
)

NOT_OK_TEXT = textwrap.dedent(f"""\
    Ex.mo(a) Senhor(a), 
        
    O arquivo que tentou obter através do Archivematica não está imediatamente disponível.
    Tentámos recuperar o mesmo, contudo não foi possível. Desta forma, pedimos-lhe que entre em contacto com a nossa equipa, através do email stic-helpdesk@ua.pt.
    
    Obrigado,
    Arquivo Geral da Universidade de Aveiro

    -----------------------------

    Hello, 

    ....
    < mensagem em ingles aqui>
    """
                          )
