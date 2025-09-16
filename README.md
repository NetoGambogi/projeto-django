# projeto-django
Projeto de gestão de chamados em Django.

Oque é necessário fazer:

Criar um projeto em django que tenha cadastro de usuários (roles: requerente, responsável, admin)
Criar um dashboard para cada role;

Requerentes podem criar chamados (Título, descrição, anexo)
-> podem excluir se os chamados ainda não estiver em atendimento
-> pode editar as informações descritivas do chamado

Responsáveis podem aceitar chamados criados pelos requerentes
-> podem editar o status do chamado para concluído ou cancelado
-> pode descrever a solução, anexar arquivos ao concluir, caso queira

Admin deve ter uma listagem de chamados e usuários

Usuários 
-> filtro por nome, role
-> pode editar informações de usuários (nome, email, role)
-> pode desativar usuários

Chamados 
-> filtro por status, código do chamado
-> pode retornar o chamado pra fila caso esteja em andamento ou cancelado (bloqueado se estiver aberta, ou concluída)
-> pode editar o responsável, requerente do chamado
-> pode excluir qualquer chamado